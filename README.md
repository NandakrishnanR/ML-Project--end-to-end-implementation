ML Project — End-to-end implementation

This repository contains a Jupyter notebook `app.ipynb` demonstrating an end-to-end ML workflow using the California housing dataset. The root also contains a serialized model `regmodel.pkl` and the runtime `requirements.txt`.

Quick start
1. Create and activate a Python virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. (Optional) Start Jupyter Lab and open `app.ipynb`:

```bash
python -m pip install jupyterlab ipykernel
python -m ipykernel install --user --name ml-project --display-name "ml-project"
jupyter lab
```

Files kept at repository root:
- `app.ipynb` — main notebook
- `regmodel.pkl` — example pickled model
- `requirements.txt` — project dependencies
- `.gitignore` — ignore rules
- `README.md` — this file

If you want me to also re-install the project dependencies into a new venv or commit these cleanup changes to a branch, tell me and I'll proceed.
