# Imagen base
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY . /app

# Instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponer el puerto en el que correrá Flask
EXPOSE 5000

# Comando de arranque
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
