# Infra va Tech Stack trong `C:\VSS`

Ngay quet: `2026-06-15`

## Tong quan kien truc

He thong trong `C:\VSS` dang co cau truc theo mo hinh nhieu service cung chia se mot local Docker network:

- Docker network dung chung: `localnetwork`
- Database chinh: PostgreSQL
- Cache/session/job support: Redis
- Message broker cho Celery va async jobs: RabbitMQ
- Frontend chinh:
  - `ui` tren Quasar/Vue
  - `3d-gallery` tren Nuxt 4 + Three.js
- Backend chinh:
  - `service-api` la business core
  - `user-management` la account/identity service
  - `bff-mobile` la mobile BFF
  - `hrm-integrate`, `sis-integrate`, `sns-integrate` la integration services

## Shared infra

### 1. PostgreSQL

- Thu muc: `C:\VSS\postgresql`
- Runtime: `postgres:latest`
- Compose: `postgresql/docker-compose.yml`
- Port host: `5432 -> 5432`
- Volume:
  - `./postgres_data`
  - `./logs`
- Co custom config qua `./init/postgresql.conf`

Vai tro:

- database dung chung cho nhieu backend
- trong env sample co thay cac DB rieng cho:
  - `crm_db` (`service-api`)
  - `crm_user` (`user-management`)
  - `sis_integrate`
  - `hrm_integrate`
  - `sns_integrate`

### 2. Redis

- Thu muc: `C:\VSS\redis`
- Runtime:
  - Redis server build tu `redis/Dockerfile`
  - RedisInsight UI: `redis/redisinsight:latest`
- Compose: `redis/docker-compose.yml`
- Port host:
  - `6379 -> 6379`
  - `5540 -> 5540` cho RedisInsight
- Volume:
  - `./redis_data`
  - `./redis_insight_data`
  - `./logs`

Vai tro:

- cache
- co the dung cho token/session support
- duoc tham chieu boi `service-api`, `user-management`, `hrm-integrate`, `sis-integrate`, `bff-mobile`

### 3. RabbitMQ

- Thu muc: `C:\VSS\rabbitmq`
- Runtime: `rabbitmq:latest`
- Compose: `rabbitmq/docker-compose.yml`
- Port host:
  - `5672 -> 5672`
  - `15672 -> 15672`

Vai tro:

- broker cho Celery workers/beat
- thay duoc trong env va compose cua:
  - `service-api`
  - `hrm-integrate`
  - `sis-integrate`
  - `sns-integrate`

## Tech stack theo project

## 1. `service-api`

- Loai: backend monolith
- Runtime image: `python:3.13`
- Framework:
  - Django 6.0.1
  - Django REST Framework
  - Celery
- Build/runtime:
  - `Dockerfile`
  - `docker-compose.yml`
- Port host: `8080 -> 8000`
- Process trong compose:
  - Django dev server
  - Celery worker
  - Celery beat

### Thu vien va stack chinh

- Database: PostgreSQL (`psycopg[binary]`)
- Queue/cache: Redis + RabbitMQ/Celery
- Data processing: `pandas`, `openpyxl`
- Security/auth: `djangorestframework-simplejwt`, `cryptography`
- Media/image:
  - `Pillow`
  - `pillow-heif`
  - `opencv-python-headless`
  - `rembg`
  - `onnxruntime`
- PDF/document/export:
  - `WeasyPrint`
  - `qrcode`
  - `vobject`
- Utilities:
  - `RapidFuzz`
  - `phonenumbers`
  - `beautifulsoup4`
  - `boto3`

### Infra lien quan

- phu thuoc `db_postgres`
- phu thuoc `vs-redis`
- phu thuoc `rabbit`
- goi service noi bo:
  - `USER_API`
  - `SIS_API`
  - `SNS_API`
  - `HRM_API`
  - `CAP_API`
  - mobile API

### Nhan xet

- Day la service co stack nang nhat va da nang nhat.
- Khong chi la CRUD API ma con chay scheduler, worker, import/export, payment callback, va image-processing.

## 2. `user-management`

- Loai: backend account/identity service
- Runtime image: `python:3.12.8`
- Framework:
  - Django 5.1.4
  - Django REST Framework
  - Celery
- Build/runtime:
  - `Dockerfile`
  - `docker-compose.yml`
- Port host: `8003 -> 8000`
- Process trong compose:
  - Django dev server
  - Celery worker

### Thu vien va stack chinh

- Database: PostgreSQL
- Cache: Redis
- Auth:
  - JWT
  - Google OAuth
  - OTP/reset flow
- API protection:
  - throttling/rate limit
- Tich hop:
  - CRM API
  - SNS API
  - CAP API
  - Mobile API

### Infra lien quan

- phu thuoc `db_postgres`
- phu thuoc `vs-redis`
- khong thay compose worker beat rieng, nhung co Celery worker trong command container

### Nhan xet

- Tach rieng khoi `service-api` de xu ly identity va user domain.
- Stack giong backend Django core, nhung nhe hon `service-api`.

## 3. `bff-mobile`

- Loai: FastAPI BFF
- Runtime image: `python:3.12.9-slim-bookworm`
- Framework:
  - FastAPI
  - Pydantic Settings
  - HTTPX
  - Redis client
- Build/runtime:
  - `Dockerfile`
  - `docker-compose.yml`
- Port host: `8009 -> 8000`
- Process trong compose:
  - `uvicorn main:app --reload`

### Thu vien va stack chinh

- FastAPI cho API layer
- `httpx` de goi service khac
- `redis` cho cache
- `PyJWT`, `cryptography` cho auth/verification
- `msgspec` cho schema/performance

### Infra lien quan

- khong co database rieng trong compose
- dung Redis qua env
- goi service:
  - `SERVICE_API`
  - `USER_API`
  - `SIS_API`
  - `HRM_API`
  - `CAP_API`

### Nhan xet

- Day la service orchestration.
- Infra nhe, it persistence noi bo, phu thuoc manh vao cac backend khac.

## 4. `sns-integrate`

- Loai: FastAPI notification service
- Runtime image: `python:3.12.9-slim-bookworm`
- Framework/layer:
  - FastAPI
  - SQLAlchemy 2
  - Alembic
  - Celery
  - Dependency Injector
- Build/runtime:
  - `Dockerfile`
  - `docker-compose.yml`
- Port host: `8008 -> 8000`
- Process trong compose:
  - FastAPI app
  - Celery worker cho email
  - Celery beat

### Thu vien va stack chinh

- Database:
  - async PostgreSQL qua `asyncpg`
  - sync PostgreSQL qua `psycopg2`
- Messaging:
  - RabbitMQ
  - Celery
- Email/SMS:
  - SMTP/SES style config
  - SMS gateway ngoai
- AWS libs:
  - `boto3`

### Infra lien quan

- phu thuoc PostgreSQL rieng cho SNS
- phu thuoc RabbitMQ
- co the goi `CRM_API`

### Nhan xet

- Day la service support/background job nhieu hon la synchronous business API.
- Stack nghieng ve queue + delivery.

## 5. `sis-integrate`

- Loai: Django integration service
- Runtime image: `python:3.13.3`
- Framework:
  - Django 5.2.9
  - Django REST Framework
  - Celery
- Build/runtime:
  - `Dockerfile`
  - `docker-compose.yml`
- Port host: `8005 -> 8000`
- Process trong compose:
  - Gunicorn
  - Celery worker

### Thu vien va stack chinh

- Database: PostgreSQL
- Queue/cache:
  - Redis
  - RabbitMQ/Celery
- Data handling:
  - `pandas`
  - `openpyxl`
- External integration:
  - Oracle DB driver `oracledb`
  - PowerSchool/SIS API config

### Infra lien quan

- phu thuoc `db_postgres`
- phu thuoc `vs-redis`
- phu thuoc `rabbit`
- goi:
  - `CRM_API`
  - `PS_API`
  - `MOBILE_API`

### Nhan xet

- Service bridge cho SIS.
- Tech stack backend co queue va ETL flavor ro rang.

## 6. `hrm-integrate`

- Loai: Django integration service
- Runtime image: `python:3.13.3`
- Framework:
  - Django 6.0.1
  - Django REST Framework
  - Celery support trong requirements/env
- Build/runtime:
  - `Dockerfile`
  - `docker-compose.yml`
- Port host: `8004 -> 8000`
- Process trong compose:
  - Gunicorn
  - Celery hien dang comment trong compose chinh

### Thu vien va stack chinh

- Database: PostgreSQL
- Queue/cache:
  - Redis
  - RabbitMQ/Celery
- File/image utilities:
  - `Pillow`
  - `pillow-heif`
  - `rembg`
  - `onnxruntime`
- ETL/document:
  - `pandas`
  - `openpyxl`
  - `WeasyPrint`
- External integration:
  - MISA
  - Google Chat webhook

### Infra lien quan

- phu thuoc `db_postgres`
- phu thuoc `vs-redis`
- co cau hinh `CELERY_BROKER_URL`
- goi:
  - `CRM_API`
  - `USER_API`
  - MISA endpoints

### Nhan xet

- Tech stack thua huong nhieu tu `service-api`, nhung pham vi he hon.
- Hien tai deployment compose chinh nghieng ve web sync API hon la chay full worker stack.

## 7. `ui`

- Loai: frontend admin/client SPA
- Runtime:
  - build stage: `node:lts-alpine`
  - serve stage: `nginx:1.25-alpine`
- Framework:
  - Vue 3
  - Quasar 2
  - Pinia
  - Vue Router
  - Vue I18n
  - Axios
- Build/runtime:
  - `Dockerfile`
  - `docker-compose.yml`
  - `nginx.conf`
- Port host: `8085 -> 80`

### Frontend stack bo sung

- UI/data:
  - Vuelidate
  - Chart.js
  - Moment
  - Xlsx
- Editors/media:
  - GrapesJS
  - MJML
  - Cropper
- 3D support:
  - `three`
  - `three-custom-shader-material`

### Infra lien quan

- Nginx SPA fallback qua `try_files ... /index.html`
- build arg `BUILD_ENV=dev|uat|prod`
- frontend env cho thay:
  - local truyen `API_URL=http://localhost:8080/`
  - local truyen `API_USER_URL=http://localhost:8003/`

### Nhan xet

- Frontend co stack application dashboard day du.
- Runtime rat don gian: build static files, serve qua Nginx.

## 8. `3d-gallery`

- Loai: frontend Nuxt app
- Runtime:
  - build/dev: `node:22-alpine`
  - prod runner: `node:22-alpine`
- Framework:
  - Nuxt 4
  - Vue 3
  - TresJS / Three.js
  - Tailwind CSS 4
  - Nuxt UI
- Build/runtime:
  - `Dockerfile`
  - `docker-compose.yml`
- Port host mac dinh: `3003 -> 3000`

### Frontend stack bo sung

- `@nuxtjs/i18n`
- `@nuxtjs/color-mode`
- `@nuxt/fonts`
- `@fingerprintjs/fingerprintjs`
- `pnpm` qua `corepack`
- `dumb-init` trong image production

### Infra lien quan

- chay theo multi-stage Dockerfile:
  - `deps`
  - `dev`
  - `build`
  - `prod`
- env cho thay service dependency chinh:
  - `NUXT_PUBLIC_CRM_API`
- compose cho phep doi:
  - `TARGET`
  - `ENV_FILE`
  - `HOST_PORT`

### Nhan xet

- Deployment pipeline sach va hien dai hon `ui`.
- Khong can Nginx; Nuxt/Nitro server tu serve tren port 3000.

## So do phu thuoc muc cao

### Core app dependency

- `ui` -> `service-api`
- `ui` -> `user-management`
- `3d-gallery` -> `service-api` (`post-3d`)
- `bff-mobile` -> `service-api`
- `bff-mobile` -> `user-management`
- `bff-mobile` -> `sis-integrate`
- `bff-mobile` -> `hrm-integrate`
- `sns-integrate` -> `service-api` (mot so callback/noi bo)
- `service-api` -> `user-management`
- `service-api` -> `sis-integrate`
- `service-api` -> `sns-integrate`
- `service-api` -> `hrm-integrate`

### Shared platform dependency

- `service-api` -> PostgreSQL / Redis / RabbitMQ
- `user-management` -> PostgreSQL / Redis
- `sns-integrate` -> PostgreSQL / RabbitMQ
- `sis-integrate` -> PostgreSQL / Redis / RabbitMQ
- `hrm-integrate` -> PostgreSQL / Redis / RabbitMQ
- `bff-mobile` -> Redis

## Muc do truong thanh cua infra

- Docker Compose duoc dung dong bo tren gan nhu tat ca project.
- Cac backend da tach service ro rang, nhung van chia se cung local network va local infra.
- Co hai phong cach runtime backend:
  - Django + Gunicorn/Celery
  - FastAPI + Uvicorn/Celery
- Frontend co hai huong:
  - SPA build ra static asset + Nginx (`ui`)
  - Nuxt runtime server (`3d-gallery`)

## File tham chieu chinh

- `C:\VSS\postgresql\docker-compose.yml`
- `C:\VSS\redis\docker-compose.yml`
- `C:\VSS\rabbitmq\docker-compose.yml`
- `C:\VSS\service-api\Dockerfile`
- `C:\VSS\service-api\docker-compose.yml`
- `C:\VSS\service-api\requirements.txt`
- `C:\VSS\service-api\.env.sample`
- `C:\VSS\user-management\Dockerfile`
- `C:\VSS\user-management\docker-compose.yml`
- `C:\VSS\user-management\requirements.txt`
- `C:\VSS\user-management\.env.sample`
- `C:\VSS\bff-mobile\Dockerfile`
- `C:\VSS\bff-mobile\docker-compose.yml`
- `C:\VSS\bff-mobile\requirements.txt`
- `C:\VSS\bff-mobile\.env.sample`
- `C:\VSS\sns-integrate\Dockerfile`
- `C:\VSS\sns-integrate\docker-compose.yml`
- `C:\VSS\sns-integrate\requirements.txt`
- `C:\VSS\sns-integrate\.env.sample`
- `C:\VSS\sis-integrate\Dockerfile`
- `C:\VSS\sis-integrate\docker-compose.yml`
- `C:\VSS\sis-integrate\requirements.txt`
- `C:\VSS\sis-integrate\.env.sample`
- `C:\VSS\hrm-integrate\Dockerfile`
- `C:\VSS\hrm-integrate\docker-compose.yml`
- `C:\VSS\hrm-integrate\requirements.txt`
- `C:\VSS\hrm-integrate\.env.sample`
- `C:\VSS\ui\Dockerfile`
- `C:\VSS\ui\docker-compose.yml`
- `C:\VSS\ui\nginx.conf`
- `C:\VSS\ui\vue-app\package.json`
- `C:\VSS\ui\vue-app\.env.local`
- `C:\VSS\3d-gallery\nuxt-app\Dockerfile`
- `C:\VSS\3d-gallery\nuxt-app\docker-compose.yml`
- `C:\VSS\3d-gallery\nuxt-app\package.json`
- `C:\VSS\3d-gallery\nuxt-app\.env.example`
