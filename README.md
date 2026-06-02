# Support Ticket Management System

Simple Django-based support ticket management system.

Requirements
- Python 3.x
- MySQL (optional) or SQLite (default)
- See `requirements.txt`

Quick start

1. Create a virtualenv and install dependencies:

```bash
pip install -r requirements.txt
```

2. Configure MySQL (optional) by setting environment variables:

- `MYSQL_NAME`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_PORT`

3. Run migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

4. Run the development server:

```bash
python manage.py runserver
```

Notes
- Default settings use SQLite for convenience. To use MySQL, export the env vars listed above.
- Login at `/accounts/login/`.

Docker (optional)

Build and run the app with Docker Compose (starts MySQL and the Django app):

```bash
docker compose build
docker compose up
```

The web app will be available at http://localhost:8000. Default DB credentials are set in `docker-compose.yml` and can be changed there or via environment variables.
