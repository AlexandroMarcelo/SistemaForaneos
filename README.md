# **ITESM Student Program**
---

##### Integrantes:
1. Daniel Pelagio
2. Alexandro Francisco Marcelo González
3. Luis Carrasco


---
## 1. Aspectos generales

### 1.1 Requerimientos técnicos

A continuación se mencionan los requerimientos técnicos mínimos del proyecto, favor de tenerlos presente para que cumpla con todos.

* El equipo tiene la libertad de elegir las tecnologías de desarrollo a utilizar en el proyecto, sin embargo, debe tener presente que la solución final se deberá ejecutar en una plataforma en la nube. Puede ser  [Google Cloud Platform](https://cloud.google.com/?hl=es), [Azure](https://azure.microsoft.com/en-us/) o AWS [AWS](https://aws.amazon.com/es/free/).
* El proyecto debe utilizar al menos dos modelos de bases de datos diferentes, de los estudiados en el curso.
* La solución debe utilizar una arquitectura de microservicios. Si no tiene conocimiento sobre este tema, le recomiendo la lectura [*Microservices*](https://martinfowler.com/articles/microservices.html) de [Martin Fowler](https://martinfowler.com).
* La arquitectura debe ser modular, escalable, con redundancia y alta disponibilidad.
* La arquitectura deberá estar separada claramente por capas (*frontend*, *backend*, *API RESTful*, datos y almacenamiento).
* Los diferentes componentes del proyecto (*frontend*, *backend*, *API RESTful*, bases de datos, entre otros) deberán ejecutarse sobre contenedores [Docker](https://www.docker.com/) y utilizar [Kubernetes](https://kubernetes.io/) como orquestador.
* Todo el código, *datasets* y la documentación del proyecto debe alojarse en un repositorio de GitHub siguiendo al estructura que aparece a continuación.

### 1.2 Estructura del repositorio
El proyecto debe seguir la siguiente estructura de carpetas:
```
- / 			        # Raíz de todo el proyecto
    - README.md			# Archivo con los datos del proyecto (este archivo)
    - frontend			# Carpeta con la solución del frontend (Web app)
        -app.py
    - api			# Carpeta con la solución de la API
        -backend
    - datasets		        # Carpeta con los datasets y recursos utilizados (csv, json, audio, videos, entre otros)
    - dbs			# Carpeta con los modelos, catálogos y scripts necesarios para generar las bases de datos
```

## 2. Descripción del proyecto

Diseñamos una página web que simula un club deportivo local, que tiene usuarios, clases e instructores. Un administrador se encarga de dar de alta a un usuario al momento de inscripción, esta se hace de manera local, y también tiene el poder de darlo de baja. Un administrador también se encarga de añadir a los instructores contratados. Cada instructor es responsable por las clases que crea e imparte y a quien inscribe y en caso de querer eliminar una clase, tiene que ponerse en contacto con un administrador.
Los usuarios pueden consultar las clases a las que están inscritos, así como las dietas que le son recomendadas por sus instructores. Para que un usuario se inscriba a una clase, debe contactar por correo electrónico a un instructor que la imparte, de esta manera queda a discreción de cada instructor el aceptar a cada usuario a su clase, como en los casos de sobrecupo. Se fomenta la comunicación por correo para iniciar la comunicación usuario-instructor para que se aclaren los contenidos de la clase, así como el instructor pueda cuestionar al usuario sobre asuntos pertinentes a la clase (nivel, condición física, etc.). 

## 3. Solución

A continuación, aparecen descritos los diferentes elementos que forman parte de la solución del proyecto.

### 3.1 Modelos de *bases de datos* utilizados

Se eligió usar MongoDB usando el servicio cloud Atlas para el manejo de la información de estudiantes, clases,  instructores. Y Redis usando el servicio cloud Redis Labs para el manejo de usuarios, representados por su correo, y sus contraseñas.

La razón para usar MongoDB es que su estructura basada en documentos permite más flexibilidad para añadir información, además que el usar un servicio cloud permite tener la información respaldada.

Se usó Redis para guardar correo y contraseña, usando hash SHA-256, ya que es una base de datos de llave valor y permite la fácil recuperación de datos.

### 3.2 Arquitectura de la solución

Se crea un contenedor con la API y el frontend, estos se conectan con las bases de datos de manera remota por internet. El contenedor se encuentra en un servicio cloud con la dirección IP: 35.232.11.47.

### 3.3 Frontend

Se utilizó Flask como frontend usando html.

#### 3.3.1 Lenguaje de programación
Python
#### 3.3.2 Framework
Flask
#### 3.3.3 Librerías de funciones o dependencias
Para instalar en python, las cuales son librerias que dependen de nuestro proyecto:
pip install flask
pip install flask_wtf
pip install flask_api
pip install dnspython
pip3 install pandas
pip3 install csvvalidator
### 3.4 Backend

Se desarrollo en python, utilizando clases y funciones para lograr comunicar las bases de datos con el frontend mediante el uso de una API.

#### 3.4.1 Lenguaje de programación
Python
#### 3.4.2 Framework
Flask
#### 3.4.3 Librerías de funciones o dependencias
Para instalar en python, las cuales son librerias que dependen de nuestro proyecto:
pip install flask
pip install flask_wtf
pip install flask_api
pip install dnspython

### 3.5 API

Se desarrollo en Python utilizando Flask. Cada enpoint está protegido para que únicamente quien tenga permiso de acceso pueda usarlo.

#### 3.5.1 Lenguaje de programación
Python
#### 3.5.2 Framework
Flask

## 3.6 Pasos a seguir para utilizar el proyecto

To launch the api to Azure, log in in your account and create a resource group, the in the terminal (at the top of your dashboard) clone this github repository in the user root (/home/<user_name>/), and cd to the APISistemaForaneos folder created by git clone, then run the following command:

    az webapp up --sku F1 -n apistudentexchange -l centralus
 
Wait for the status of the page (json). Copy the URL given by the previous command, and save it

Finally change the Startup Command of the appservice in App Services -> apistudentexchange -> Configuration (left panel) -> General Settings -> Startup Command, by typing the following:

    gunicorn --bind=0.0.0.0 --timeout 600 app:app

Wait some minutes and finally go to the URL given and thats all.

Locally clone the repo of the api: https://github.com/AlexandroMarcelo/APISistemaForaneos 
and the project https://github.com/AlexandroMarcelo/SistemaForaneos
Change the port of the app to 5050
and change the URL of the GradesApi to localhost:5050
Finally run each project individually with python3

## 4. Referencias

http://flask.pocoo.org/docs/0.12/patterns/flashing/

https://wtforms.readthedocs.io/en/stable/

http://api.mongodb.com/python/current/api/pymongo/collection.html
