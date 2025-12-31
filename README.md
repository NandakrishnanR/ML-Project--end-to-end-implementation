ML Project — End-to-end implementation `Development` to `staging` to `preprod` to `production`
=====================================

This repository demonstrates a small end-to-end machine learning project using the California Housing dataset. It contains the training notebook, saved model artifacts, a minimal Flask app for serving predictions, and simple deployment wiring.

What is included
- `app.ipynb` — Jupyter notebook that walks through data loading, preprocessing, training, evaluation and saving model/scaler artifacts.
- `main.py` — Minimal Flask application that exposes a prediction endpoint and serves a small HTML dashboard (templates/).
- `regmodel.pkl` and `scaler.pkl` — Pickled model and scaler (created from the notebook). The app expects these files to be present for prediction.
- `requirements.txt` — Python packages required to run the project.
- `.gitignore` — common ignore rules for Python projects.
- `templates/home.html` — Simple web dashboard to call the prediction API.
- `Procfile` — Process declaration used by some PaaS providers (Heroku, Railway, Render). See "Procfile" section below.

Quick start — run locally
-------------------------
These steps assume macOS / Linux. Windows users can adapt the venv commands accordingly.

1. Clone the repo and change into the project folder:

```bash
cd "/Users/nandu/PycharmProjects/ML-end to end implementation/ML-Project--end-to-end-implementation"
```

2. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

4. Start the Flask app (development server):

```bash
source .venv/bin/activate
python main.py
```

Open http://127.0.0.1:5000/ in your browser to view the dashboard. The prediction API is available at `POST /predict` (see API section).

API — predict endpoint
----------------------
Endpoint: `POST /predict`

- Accepts JSON payload with the features for one sample. Two formats are supported:

	1) Feature dictionary (recommended):

```json
{
	"MedInc": 8.3252,
	"HouseAge": 41.0,
	"AveRooms": 6.984127,
	"AveBedrms": 1.023810,
	"Population": 322.0,
	"AveOccup": 2.555556,
	"Latitude": 37.88,
	"Longitude": -122.23
}
```

	2) Wrapped under `data` key (older client format):

```json
{ "data": { /* same dict as above */ } }
```

Response (JSON):

```json
{ "prediction": 4.23 }
```

Notes about the prediction value
- The California housing target in scikit-learn is in units of 100,000 USD. So `4.23` corresponds to approximately $423,000.
- The app expects the model to have been trained with the same feature ordering and scaling. The repository includes `scaler.pkl` and `regmodel.pkl` saved from the notebook; keep them next to `main.py`.

Model artifacts and pickling
---------------------------
- `scaler.pkl` — the fitted `StandardScaler` used to standardize features during training.
- `regmodel.pkl` — the trained `LinearRegression` model.

Two common deployment patterns:
1. Two files (scaler + model): load both in the server, call `scaler.transform()` on incoming raw features, then `model.predict()`.
2. Single pipeline file: build an `sklearn.pipeline.Pipeline([('scaler', StandardScaler()), ('model', LinearRegression())])`, fit it on raw features and `joblib.dump(pipeline, 'pipeline.pkl')`. At inference time call `pipeline.predict(raw_features)` — this is safer and reduces chances of forgetting to scale.

This project currently saves scaler and model separately (check the final notebook cells) — either approach is fine; pick one and keep the server and client consistent.

Procfile — what it is and why it’s included
-----------------------------------------
A `Procfile` is a plain text file used by several Platform-as-a-Service (PaaS) providers (for example Heroku, Railway, Render) to declare process types and the command that should be run to start your application. The most common process type is `web`, which handles HTTP traffic.

Example `Procfile` content for this Flask app:

```
web: gunicorn main:app
```

What this does:
- `web` is the process type the platform routes HTTP traffic to.
- `gunicorn main:app` tells the PaaS to use Gunicorn (a production-ready WSGI server) to run the `app` object from `main.py`.

Why use a Procfile?
- Local development often uses Flask’s built-in server (`python main.py`) which is convenient but not suitable for production. A Procfile lets the PaaS know how to start the app with a production server.
- Including a `Procfile` makes deploying to Heroku (or similar) simple: the platform reads the file and runs the declared command on each dyno/container.

Deployment notes
----------------
- For production, prefer `gunicorn` or `uvicorn` behind a reverse proxy. Example: `gunicorn --workers 3 --bind 0.0.0.0:$PORT main:app`.
- Ensure your production environment has the same Python and package versions (use `requirements.txt` and pin versions).
- Do not run `debug=True` in production — it enables an interactive debugger and exposes code execution.

Troubleshooting & common issues
-------------------------------
- 403 Forbidden in Postman but curl works: check Postman proxy/interceptor settings, remove extra headers, and ensure you use `http://127.0.0.1:5000` (some proxies treat `localhost` differently).
- 500 errors when POSTing JSON: confirm the body shape matches what the server expects (`data` key or direct feature dict), and that `scaler.pkl` and `regmodel.pkl` are present.
- Pickle load errors: confirm you are using compatible Python and scikit-learn versions when saving/loading pickles. Prefer `joblib` for sklearn artifacts.

Security and best practices
---------------------------
- Never unpickle data from untrusted sources — unpickling executes code contained in the pickle.
- Lock dependency versions and reproduce the runtime (use the same Python minor version where possible).
- Add input validation and rate limiting in production to prevent abuse.

Reproducing training
---------------------
Open `app.ipynb` and run the cells in order. The notebook:
1. Fetches the California housing dataset.
2. Converts to a pandas DataFrame and splits into `X` and `y`.
3. Performs train/test split and scales features with `StandardScaler`.
4. Trains a `LinearRegression` model.
5. Saves the fitted `scaler` and `model` with `pickle.dump` (see final cell).




License
-------
This repository is provided as-is for demonstration and learning purposes.

