# Game Guides - API Python

Backend del proyecto Game Guides desarrollado con Python 3.12 + FastAPI y PostgreSQL, siguiendo el patrón Senior.

---

## Requisitos

- Python 3.12+
- PostgreSQL
- [Google Auth](https://console.cloud.google.com)

---

## Instalación

### 1. Clonar y crear entorno virtual
```sh
git clone <repo-url>
cd repo_folder
py -m venv .venv
.venv\Scripts\activate
deactivate
```

### 2. Instalar dependencias
```sh
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary python-dotenv pydantic pydantic-settings
pip install google-auth google-auth-oauthlib google-auth-httplib2
pip install pydantic[email]
pip install python-jose[cryptography]
```
### 3. (Opcional) Dependencias de test
```sh
pip install pytest httpx
```

Guardar dependencias:
```sh
pip freeze > requirements.txt
```

Instalar desde requirements:
```sh
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Crear archivo `.env` basado en `.env_demo`:
```sh
cp .env_demo .env
```

Editar `.env` con tus credenciales:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/data_base
SECRET_KEY=your-secret-key-here
CLOUDINARY_URL=cloudinary://...
```

### 4. Generar SECRET_KEY
```sh
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Ejecutar

```sh
.venv\Scripts\activate
py run.py
```

O directamente:
```sh
uvicorn src.main:app --reload
```

**Swagger:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Tests

```sh
pytest tests/ -v
```

Requiere base de datos PostgreSQL configurada en `.env` (usa `DATABASE_URL`).

---

## Arquitectura

```
pytest.ini                    → Configuración de pytest (pythonpath)
tests/
├── conftest.py                → Fixtures: DB, TestClient, cleanup
├── test_auth.py               → Auth: google, refresh, logout (10 tests)
├── test_genres.py             → Genres CRUD (11 tests)
└── test_platforms.py          → Platforms CRUD (11 tests)
src/
├── main.py                      → FastAPI app, CORS, exception handlers, routers
├── core/                        → Cross-cutting (transversal)
│   ├── config.py                →   Pydantic settings (DATABASE_URL, SECRET_KEY, etc.)
│   ├── database.py              →   SQLAlchemy engine, session, Base
│   ├── exceptions.py            →   AppError, NotFoundError, DuplicateNameError
│   └── security.py              →   JWT create/verify, get_current_user, OAuth2 scheme
├── models/
│   └── models.py                → SQLAlchemy entidades (User, Role, Platforms, Genre...)
├── schemas/
│   └── dtos.py                  → Pydantic DTOs compartidos (AppModel, PaginationResponse, etc.)
├── api/
│   ├── auth/                    → Feature: autenticación
│   │   ├── routes.py            →   endpoints
│   │   ├── schemas.py           →   DTOs específicos
│   │   ├── service.py           →   lógica de negocio
│   │   └── google_service.py    →   validación Google OAuth
│   ├── platforms/               → Feature: plataformas
│   │   ├── routes.py            →   GET/POST/PUT/DELETE
│   │   ├── service.py           →   lógica
│   │   └── repository.py        →   queries SQLAlchemy
│   └── genres/                  → Feature: géneros
│       ├── routes.py
│       ├── service.py
│       └── repository.py
└── ...próximos features (games, guides, characters, etc.)
```

### Principios
- **Feature-based**: cada funcionalidad encapsulada en `api/{feature}/`
- **Separación**: route → service → repository
- **Route** decide HTTP (200, 201, 204, 404)
- **Service** orquesta y aplica reglas de negocio
- **Repository** solo consultas SQLAlchemy
- **Cross-cutting** en `core/` (config, security, exceptions)
- **Errores**: `AppError` → middleware centralizado en `main.py`

