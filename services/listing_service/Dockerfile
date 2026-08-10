FROM python:3.12-slim

WORKDIR /app


COPY services/listing_service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY services/listing_service/ .
COPY shared/ /app/shared/

# python -m uvicorn src.app:app --port 80 --host 0.0.0.0 --app-dir src
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
