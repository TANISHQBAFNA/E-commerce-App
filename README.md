# VTEssentials (Django ecommerce)

Catalog, cart, users/auth, and admin-review flows for a class ecommerce app. This branch is a **framework/toolchain upgrade only** — templates and static assets are unchanged (visual polish is out of scope).

## Runtime

| Piece | Was | Now |
| --- | --- | --- |
| Python | 3.9.0 | 3.12 (`runtime.txt`: `python-3.12.11`) |
| Django | 3.2.9 | **5.2.17 LTS** |
| gunicorn | 20.1.0 | 26.2.0 |
| whitenoise | 5.3.0 | 6.12.0 |
| Pillow | 8.4.0 | 12.3.0 |
| Postgres driver | `psycopg2==2.9.1` | `psycopg2-binary==2.9.13` |
| DB URL helper | `dj-database-url==0.5.0` + `django-heroku==0.3.1` | `dj-database-url==3.1.2` (django-heroku removed) |

## Run locally

Python 3.12 required.

```bash
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata VT/fixtures/catalog.json
python manage.py createsuperuser   # optional, Django admin at /admin/
python manage.py runserver
```

Open http://127.0.0.1:8000/

Create a store admin (session role, separate from Django staff):

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from users.models import details
u = User.objects.create_user('admin', password='changeme', first_name='Admin', last_name='Admin')
details.objects.create(user=u, role='admin')
```

Then log in with the navbar form. Register creates a `regular` user.

## Verify

```bash
python -m pip check
python manage.py check
python manage.py test
```

Optional freeze snapshot (compare to `requirements.txt`):

```bash
python -m pip freeze
```

## Heroku-style config (not deployed here)

`Procfile` still runs `gunicorn Project.wsgi`. `django-heroku` is gone; set env instead of that package mutating settings:

| Env var | Purpose |
| --- | --- |
| `SECRET_KEY` | Production secret |
| `DEBUG` | `false` in production |
| `ALLOWED_HOSTS` | comma-separated hosts |
| `CSRF_TRUSTED_ORIGINS` | comma-separated origins **with scheme** (Django 4+) |
| `DATABASE_URL` | Postgres URL; local default is SQLite |
| `DATABASE_SSL` | default `true` when `DATABASE_URL` is set |

WhiteNoise still serves static files. Production uses `CompressedStaticFilesStorage`; run `python manage.py collectstatic` on deploy.

## App map

- `VT` — catalog, product CRUD, cart AJAX (`cart_items` counter)
- `users` — register, profile, admin user/review management
- `actions` — activity feed (`Action` + generic relation)

Named URL namespaces match the existing templates: `VTessential:` and `user:` / `users:`.

## Notes

- `requirements.txt` is UTF-8 (it was UTF-16).
- `USE_L10N` removed (Django 5).
- `DEFAULT_AUTO_FIELD` remains `BigAutoField`.
- `STORAGES['staticfiles']` replaces `STATICFILES_STORAGE`.
- SQLite is the local default. The old checked-in `db.sqlite3` is gitignored (stale schema vs later models).
- `views.py` / `models.py` / `urls.py` for `VT` (and models/urls/views for `users` / `actions`) were never in git history (web “Add files via upload”). They are restored from templates, migrations, and `p5.json` so the upgraded app actually boots. Templates/CSS/JS were not redesigned.
