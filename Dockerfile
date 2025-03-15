# Usa una imagen ligera y compatible
FROM python:3.10-slim-bullseye

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala mysqlclient manualmente antes de instalar requirements.txt
RUN pip install --no-cache-dir mysqlclient

# Crea un entorno virtual y activa
RUN python -m venv venv && . venv/bin/activate

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Recoge archivos estáticos
RUN python manage.py collectstatic --noinput

# Aplica migraciones
RUN python manage.py migrate

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar Django con Gunicorn
CMD ["gunicorn", "kardex.wsgi:application", "--bind", "0.0.0.0:8000"]
