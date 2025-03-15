# Usa una imagen ligera y compatible
FROM python:3.10-slim-bullseye

# Establece el directorio de trabajo en /app
WORKDIR /app

# Instala dependencias del sistema necesarias para mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libmariadb-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos del proyecto al contenedor
COPY . .

# Crea un entorno virtual
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
