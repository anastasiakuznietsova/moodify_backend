import joblib
import pandas as pd


def get_embeddings(texts):
    tfidf_model = joblib.load('./ml_models/tfidf_vectorizer.joblib')
    if isinstance(texts, str):
        texts = [texts]
    embedded_vectors = tfidf_model.transform(texts)
    return embedded_vectors.toarray().tolist()


def get_preprocessed_metadata(song_data):
    df = pd.DataFrame(song_data)
    df = df.drop(columns=["Title", "Artist"])
    if 'text' in df.columns:
        df['text'] = df['text'].fillna("")
    df = pd.get_dummies(df, columns=['Genre', 'Key', 'Time_signature'])
    df['text_vector'] = get_embeddings(df['text'])
    embed_df = pd.DataFrame(df["text_vector"].tolist(),
                            columns=[f'emb_{i}' for i in range(len(df["text_vector"][0]))])

    model_cols = joblib.load('./ml_models/trained_model_columns.joblib')
    df = align_columns(df, model_cols)
    return pd.concat([df.drop(columns=["text_vector"]), embed_df], axis=1)


def align_columns(user_df, training_columns):
    missing_cols = [col for col in training_columns if col not in user_df.columns]
    if missing_cols:
        user_df = pd.concat([user_df, pd.DataFrame(0, index=user_df.index, columns=missing_cols)], axis=1)
    user_df = user_df[training_columns]
    return user_df


def get_prediction(song_features):
    label_encoding = {
        'sadness': 1,
        'joy': 2,
        'love': 3,
        'surprise': 4,
        'anger': 5,
        'fear': 6
    }
    if isinstance(song_features, dict):
        data_to_process = [song_features]
    else:
        data_to_process = song_features
    preprocessed_data = get_preprocessed_metadata(data_to_process)
    emotion_model = joblib.load('./ml_models/trained_model.joblib')
    make_prediction = emotion_model.predict(preprocessed_data)
    label_decoding = {v: k for k, v in label_encoding.items()}
    predicted_emotions = [label_decoding[i] for i in make_prediction]

    return predicted_emotions

