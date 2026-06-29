# Usamos Python 3.11 que es el "sweet spot" actual para IA y LangGraph
FROM python:3.11-slim

# Evita que Python escriba archivos .pyc y fuerza a que los logs salgan directo a la terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema operativo que ChromaDB y sqlite necesitan a veces para compilar
RUN apt-get update && apt-get install -y \
    build-essential \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]