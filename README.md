# wishagugu_web


## Running locally
```python
python3 -m venv venv
source venv/bin/activate

python manage.py migrate
python manage.py runserver
```


## Creating a superuser account
```python
python manage.py createsuperuser
```
login at `localhost:8000/admin`
