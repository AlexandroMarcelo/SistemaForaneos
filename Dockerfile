# Using lightweight alpine image
FROM python:3.6-alpine

# Installing packages
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev

# Defining working directory and adding source code
WORKDIR /usr/src/app
COPY requirements.txt ./

# Install API dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Exportar la variable de entorno FLASK_APP, apuntando a /frontend/main.py, que es donde se encuentra el ejecutable
ENV FLASK_APP=frontend/app.py

# Add application code.
COPY . ./

# Start app
EXPOSE 8080
CMD ["flask", "run", "--host=0.0.0.0"]
