FROM python:3.12-slim

WORKDIR /app

COPY services/auth_service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY services/auth_service/ .
COPY shared/ /app/shared/

# python -m uvicorn src.app:app --port 80 --host 0.0.0.0 --app-dir src
CMD ["sh", "-c", "python -m uvicorn app.main:app --port ${AUTH_PORT:-8000} --host 0.0.0.0"]