FROM python:3.10-slim

WORKDIR /code

# Install core dependencies
RUN pip install --no-cache-dir fastapi uvicorn "mlflow==2.8.1" scikit-learn numpy azure-storage-blob azure-identity

COPY ./main.py /code/main.py

# Expose port 8000 for network routing
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
