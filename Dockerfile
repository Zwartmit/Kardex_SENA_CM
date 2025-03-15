# Usa una imagen oficial de Python
FROM python:3.10

# Establece el directorio de trabajo en /app
WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    python3-dev \
    libmariadb-dev-compat \
    libmariadb-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos del proyecto a /app
COPY . .

# Crea el entorno virtual
RUN python -m venv venv && . venv/bin/activate

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Recoge los archivos estáticos
RUN python manage.py collectstatic --noinput

# Aplica migraciones a la base de datos
RUN python manage.py migrate

# Expone el puerto 8000 (usado por Django)
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "tu_proyecto.wsgi:application", "--bind", "0.0.0.0:8000"]
