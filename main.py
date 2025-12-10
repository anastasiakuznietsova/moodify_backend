from fastapi import FastAPI, HTTPException
from tornado import concurrent
from services.reccobeats import get_track_features
from schemas import SongFeatures
from services.spotify import get_playlist_tracks_ids, extract_spotify_id
from utils.count_percentage_emotion import calculate_emotion_stats
from services.trained_model_evaluation import get_prediction

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

@app.get('/analyze/playlist')
def get_playlist_analysis(url: str):
    try:
        track_ids = get_playlist_tracks_ids(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    features_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_to_id = {executor.submit(get_track_features, tid): tid for tid in track_ids}

        for future in concurrent.futures.as_completed(future_to_id):
            tid = future_to_id[future]
            try:
                data = future.result()
                if data is not None:
                    features_list.append(data)
            except Exception as exc:
                print(f"Track {tid} failed hard: {exc}")

    if not features_list:
        raise HTTPException(status_code=404, detail="No tracks could be analyzed (ReccoBeats missing data)")
    try:
        predictions = get_prediction(features_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    analyzed_tracks = []
    for i, features in enumerate(features_list):
        pred_val = predictions[i]
        if hasattr(pred_val, 'item'):
            pred_val = pred_val.item()

        result = {
            "features": features,
            "predicted_emotion": pred_val
        }
        analyzed_tracks.append(result)
    main_emotion, percentages = calculate_emotion_stats(predictions)
    return_statement = {
        'main_emotion':main_emotion,
        'percentages':percentages,
        "tracks_amount": len(predictions),
        'tracks_predictions': analyzed_tracks
    }
    return return_statement

@app.get('/get_song_parameters')
def get_song_analysis(url:str):
    try:
        track_id = extract_spotify_id(url)
    except:
        raise HTTPException(status_code=404, detail='Spotify song ID not found')
    try:
        song_features = get_track_features(track_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return song_features


@app.post("/analyze/track")
def predict_emotion(song: SongFeatures):
    song_dict = song.dict()
    try:
        prediction = get_prediction(song_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "predicted_emotion": prediction[0],
        "used_parameters": song_dict,
    }