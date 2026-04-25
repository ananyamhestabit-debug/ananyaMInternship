FROM python:3.10-slim

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# copy only requirements first (optimization)
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy full code
COPY . .

# env
ENV MODEL_PATH=/app/model/model-q4.gguf

# ports
EXPOSE 8000

# run backend only 
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]