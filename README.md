# Game Guides - API Python 3.12.x + PostgreSQL

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
python.exe -m pip install --upgrade pip
```
```sh
pip install fastapi uvicorn[standard] sqlalchemy asyncpg greenlet python-dotenv pydantic pydantic-settings
pip install google-auth google-auth-oauthlib google-auth-httplib2
pip install pydantic[email]
pip install python-jose[cryptography]
pip install slowapi
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

### 4. Configurar variables de entorno
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
│   ├── exceptions.py            →   AppError, NotFoundError, DuplicateNameError, InvalidApiKeyError
│   ├── dependencies.py          →   verify_api_key (X-Api-Key header)
│   ├── limiter.py               →   Rate limiter (slowapi)
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
- **Repository** solo consultas SQLAlchemy (async con `AsyncSession` + `asyncpg`)
- **Cross-cutting** en `core/` (config, security, exceptions, limiter, dependencies)
- **Errores**: `AppError` → middleware centralizado en `main.py`
- **API Key**: `X-Api-Key` header requerido globalmente vía `verify_api_key` en `core/dependencies.py`
- **Rate Limiting**: slowapi con default `100/minute` en todos los endpoints, `10/minute` en `/auth/google`, `/health` exento

---

## Autenticación con Google OAuth (Backend)

### Endpoints

| Método | Ruta | Request | Response |
|--------|------|---------|----------|
| POST | `/api/auth/google` | `{ googleToken: string }` | `{ token, refresh_token, user }` |
| POST | `/api/auth/refresh` | `{ refreshToken: string }` | `{ token, refresh_token }` |
| POST | `/api/auth/logout` | `{ refreshToken: string }` | `{ message }` |
| GET | `/api/auth/me` | `Authorization: Bearer <token>` | `{ id_user, email, name, picture, role }` |

### Flujo de autenticación

```
POST /api/auth/google { googleToken }
  → google_service.validate_google_token(googleToken)
      → GET https://oauth2.googleapis.com/tokeninfo?id_token=...
      → verifica aud == GOOGLE_CLIENT_ID
      → verifica email_verified
  → service: busca usuario por email en BD
      → si no existe: lo crea con role='user'
  → security.create_access_token(user_id) → JWT (30 min)
  → security.create_refresh_token(user_id) → refresh hasheado (7 días)
  → response { token, refresh_token, user }
```

### Refresh token rotation

```
POST /api/auth/refresh { refreshToken }
  → busca refresh token por hash en BD
  → si expirado o revocado → 401
  → rota: revoca el actual, crea uno nuevo
  → response { token, refresh_token }
```

### Variables de entorno

| Variable | Descripción |
|----------|-------------|
| `GOOGLE_CLIENT_ID` | Client ID de Google OAuth (mismo que PUBLIC_ del frontend) |
| `GOOGLE_CLIENT_SECRET` | Client Secret de Google |
| `JWT_SECRET_KEY` | Clave para firmar JWT (generar con `secrets.token_urlsafe(32)`) |
| `JWT_ALGORITHM` | Algoritmo JWT (`HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiración access token (30) |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Expiración refresh token (7) |
| `DATABASE_URL` | Conexión PostgreSQL (`postgresql+asyncpg://...`) |

### Estructura de archivos (auth)

```
src/api/auth/
├── routes.py           → 4 endpoints (google, refresh, logout, me)
├── schemas.py          → Pydantic: GoogleAuthRequest, TokenResponse, RefreshRequest
├── service.py          → Lógica: autenticar, refrescar, revocar
└── google_service.py   → Validación de token con Google API

src/core/
├── security.py         → JWT create/verify, hash refresh tokens, get_current_user
└── config.py           → Settings con todas las env vars

src/repositories/
└── auth.py             → Queries: upsert_user, find_refresh_token, save_refresh_token, revoke_refresh_token

src/models/
└── models.py           → User, RefreshToken (SQLAlchemy)
```

### Google token validation (`google_service.py`)

```python
async def validate_google_token(google_token: str) -> GoogleUserData:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://oauth2.googleapis.com/tokeninfo",
            params={"id_token": google_token},
        )
    if resp.status_code != 200:
        raise InvalidGoogleTokenError()
    data = resp.json()
    if data.get("aud") != settings.GOOGLE_CLIENT_ID:
        raise InvalidGoogleTokenError("aud mismatch")
    if not data.get("email_verified"):
        raise InvalidGoogleTokenError("email not verified")
    return GoogleUserData(
        email=data["email"],
        name=data.get("name", ""),
        picture=data.get("picture", ""),
    )
```

### Cómo replicar en otro proyecto

1. Copiar `src/api/auth/` completo
2. Copiar `src/core/security.py` (solo JWT + refresh)
3. Copiar `src/repositories/auth.py`
4. Agregar modelos `User` y `RefreshToken` en `src/models/models.py`
5. Agregar `src/core/exceptions.py` si no existe
6. Copiar variables de entorno al `.env`
7. Registrar el router en `main.py`: `app.include_router(auth_router, prefix="/api")`
8. Dependencias: `python-jose[cryptography]`, `httpx`, `passlib[bcrypt]`

