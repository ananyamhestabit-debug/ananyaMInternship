FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV MODEL_PATH=/app/model/model-q4.gguf

EXPOSE 8000
EXPOSE 8501

CMD bash -c "uvicorn day5.backend.app:app --host 0.0.0.0 --port 8000 & streamlit run day5/frontend/ui.py --server.port 8501 --server.address 0.0.0.0"