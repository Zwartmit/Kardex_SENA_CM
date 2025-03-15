FROM python:3.9-slim

# Usa un espejo diferente para apt-get
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libmysqlclient-dev \
    python3-dev \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Actualiza pip y setuptools
RUN pip install --upgrade pip setuptools

# Copia el archivo de requisitos
COPY requirements.txt /app/requirements.txt

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia el resto de la aplicación
COPY . /app

# Establece el directorio de trabajo
WORKDIR /app

# Ejecuta la aplicación
CMD ["python", "manage.py", "runserver"]