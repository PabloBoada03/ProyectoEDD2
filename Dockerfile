# Usa imagen base oficial de Python
FROM python:3.10-slim

# Establece directorio de trabajo
WORKDIR /app

# Copia archivos
COPY . .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exporta variable de entorno para FLASK_APP (opcional)
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Expone puerto
EXPOSE 5000

# Ejecuta la app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
