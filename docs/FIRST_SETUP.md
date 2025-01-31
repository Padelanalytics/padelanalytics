# First set up in mac book

Padelanalytics is a Django application. Follow the below steps to set up your environment and launch Django locally at your computer.

1. Install postgres with:

```bash
brew install postgresql
```

2. Activate your virtual environment:

```bash
source ./.venv/padel/bin/activate
```

3. Download the production database (or alternative use another one):

```bash
ssh-add   # add the ssh key so you can access to production
export PA_PROD_HOST=root@195.201.148.68
sh ./scripts/download_prod_db.sh
```

4. And run Django either with:

```bash
make runserver
```

or

```bash
python3 manage.py runserver
```