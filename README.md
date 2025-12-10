````markdown
# Moodify Backend

Moodify is a music emotion analysis backend that extracts features from songs using Spotify and Reccobeats APIs, fetches lyrics from Genius, and predicts the song's mood using a trained machine learning model.

---

## Features

- Retrieve song metadata and audio features from Spotify and Reccobeats
- Extract lyrics from Genius
- Predict song mood (e.g., joy, sadness, anger, etc.) using a trained model
- Handle missing data and allow user input for incomplete fields
- FastAPI auto-generated interactive API documentation via Swagger

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/moodify-backend.git
cd moodify-backend
````

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. **Extract the model files:**
   Before running the backend, make sure to extract the zip file containing the three required `.joblib` files:

* `trained_model.joblib`
* `tfidf_vectorizer.joblib`
* `trained_model_columns.joblib`

Place these files in the `utils/` folder. The backend **will not work without them**.

---

## Environment Variables

The backend requires API tokens for Spotify and Genius:

* `SPOTIFY_CLIENT_ID`
* `SPOTIFY_CLIENT_SECRET`
* `GENIUS_ACCESS_TOKEN`

You can set them in a `.env` file or export them in your shell.

---

## Running the Backend

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

### API Documentation (Swagger)

FastAPI automatically generates interactive documentation for all endpoints. Visit:

```
http://127.0.0.1:8000/docs
```

to explore the endpoints, see request/response models, and test them directly from your browser.

---

## API Endpoints

### 1. `/get_song_parameters?url=<spotify_url>`

* **Method:** GET
* **Description:** Fetches song metadata and audio features.
* **Response Example:**

```json
{
  "Explicit": 1,
  "Length": 185,
  "Genre": "pop",
  "Key": 5,
  "Tempo": 96.5,
  "Loudness (db)": -11.83,
  "Time signature": "4/4",
  "Energy": 0.179,
  "Danceability": 0.332,
  "Positiveness": 0.315,
  "Speechiness": 0.0326,
  "Liveness": 0.0886,
  "Acousticness": 0.879,
  "Instrumentalness": 0,
  "text": "Lyrics of the song..."
}
```

### 2. `/check_song?url=<spotify_url>`

* **Method:** GET
* **Description:** Fetches song metadata and returns it in a format ready for user input or prediction.

---

## Notes

* If audio features are missing from Reccobeats, the client can manually fill in fields such as `Time signature`.
* The backend preprocesses metadata and text embeddings before sending them to the prediction model.
* **Important:** To run the backend correctly, make sure the three `.joblib` files are extracted and placed in `utils/` before starting the server.
* Use the interactive Swagger docs at `/docs` to easily test endpoints and view request/response formats.

---

## Contributing

Feel free to submit issues or pull requests for improvements, bug fixes, or additional features.

---

## License

MIT License

```

I can also **highlight this requirement at the very top of the README in a “Getting Started” note**, so no one misses it. Do you want me to do that?
```
