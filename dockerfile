FROM python:3.14-slim

WORKDIR /app
COPY app.py demo.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000 8001
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
