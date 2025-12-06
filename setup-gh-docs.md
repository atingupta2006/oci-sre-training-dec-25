## Setup mk-docs
```
cd ~
git clone https://github.com/atingupta2006/oci-sre-training-dec-25
cd "oci-sre-training-dec-25"
python -m venv ~/venv
source ../venv/Scripts/activate
pip install -r requirements.txt
mkdocs new .
mkdocs  build
mkdocs gh-deploy
mkdocs gh-deploy --force
python -m mkdocs serve
# open http://127.0.0.1:8000
```

## Deploy to GitHub Pages (automatic)

1. Create a new GitHub repository (e.g., `sre-training`).
2. Push this project to the repository `main` branch.
3. GitHub Actions (included) will build and deploy the site to GitHub Pages automatically on push to `main`.

If you prefer, you can use `mkdocs gh-deploy` manually:

```bash
mkdocs gh-deploy --force
```
