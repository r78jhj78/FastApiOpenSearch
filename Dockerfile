# FROM python:3.10-slim
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY ./app ./app
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# Usamos Python 3.11 slim
# Usamos Python slim
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos solo lo necesario (sin serviceAccount.json)
COPY app/ ./app

# Actualizar pip e instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r app/requirements.txt

# Exponer puerto
EXPOSE 8000

# Comando por defecto para iniciar la app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
