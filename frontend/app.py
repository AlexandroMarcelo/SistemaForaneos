# -*- coding: utf-8 -*-
from flask import Flask,  jsonify, render_template, flash, redirect, url_for, session, request, logging  #render_template: para recargar la pagina

from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_wtf import FlaskForm
#from DBmodels import Gimnasio
#import jinja2
import os, sys
import json
sys.path.insert(0, os.path.abspath(".."))


#from api.DBmodels import Gimnasio
from api import GymAPI
from api import GradesAPI

app = Flask(__name__)
app.secret_key='12345'

api = GymAPI.GymAPI()
apiGrades = GradesAPI.GradesAPI()
nombre_usuario = ""
correo_usuario = "daniel@gmail.com" #BORRAR
logged_in_user = True
logged_in_instructor = False

#Home para todos, pero de manera que cada quien pueda ver lo suyo
@app.route('/')
def root():
    #return jsonify({'test': api.get_all_users()})
    #return jsonify({'user': apiGrades.get_user_grades('A01021383')})
    return redirect(url_for('login'))

#Home para todos, pero de manera que cada quien pueda ver lo suyo
@app.route('/home')
def home():
    if logged_in_user or logged_in_instructor:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

#Login page 
@app.route('/login', methods=['GET', 'POST'])
def login():
    #print(api.get_all_instructors())
    if request.method == 'POST':
        email = request.form['correo']
        input_password = request.form['password']
     
        #usuarios = api.get_all_users()
        #print(usuarios)

        domain = email.rsplit('@', 1)[1]
        global correo_usuario
        correo_usuario = email
        #Comparar contrasenias
        password = sha256_crypt.encrypt(str(input_password))
        print(password)
        #password_redis = api.get_password_user(email)

        password_redis = True
        print(input_password)
        
        print(password_redis)
        if domain == 'mambafit.com': #para los instructores
            if password_redis is not False: #Not found
                #if sha256_crypt.verify(input_password, password_redis):
                if True:
                    session['instructor'] = True
                    session['nombre'] = 'Instructor'
                    global logged_in_instructor
                    logged_in_instructor = True
                    return redirect(url_for('home'))
                else:
                    error = 'Usuario no encontrado'
                    return render_template('login.html', error=error)
            else: 
                error = 'Correo no encontrado'
                return render_template('login.html', error=error)
        #Users
        else:
            global nombre_usuario
            nombre_usuario = api.get_name_user(email)
            #print(correo_usuario)
            if password_redis == False: #Not found
                error = 'Correo no encontrado'
                return render_template('login.html', error=error)
            else: 
                #if sha256_crypt.verify(input_password, password_redis):
                #Aqui
                #if True:
                app.logger.info('VALIDO')
                session['logged_in'] = True
                session['nombre'] = nombre_usuario
                global logged_in_user
                logged_in_user = True
                return redirect(url_for('home'))
                '''
                else:
                    error = 'Usuario no encontrado'
                    app.logger.info('NO VALIDO')
                    return render_template('login.html', error=error)
                '''
    
    print(api.get_all_users())
    return render_template('login.html')

#Logout
@app.route('/logout')
def logout():
    session.clear()
    global nombre_usuario
    nombre_usuario = ""
    global correo_usuario
    correo_usuario = ""
    global logged_in_user
    logged_in_user = False
    global logged_in_instructor
    logged_in_instructor = False
    return redirect(url_for('login'))

#Apartado para saber el perfil de usuario
@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if logged_in_user:
        #Just to get the total of weeks for the dropdown 
        current_week = request.form.get('current_week')
        if current_week == None:
            current_week = 0
        current_week = int(str(current_week))
        user_grades = apiGrades.get_user_grades(correo_usuario, current_week)
        total_weeks = apiGrades.get_total_weeks()
        weeks = []
        helper_weeks = 1
        while helper_weeks <= total_weeks:
            weeks.append(helper_weeks)
            helper_weeks = helper_weeks + 1

        #Filling the lists for the grades for the user
        class_name = []
        academic_grade = []
        team_work_grade = []
        communication_skill_grade = []
        for grades in user_grades:
            class_name.append(grades['class'])
            academic_grade.append(grades['academic'])
            team_work_grade.append(grades['teamWork'])
            communication_skill_grade.append(grades['communication'])
        return render_template('perfil.html', weeks=weeks, class_name=class_name, academic_grade=academic_grade, team_work_grade=team_work_grade, communication_skill_grade=communication_skill_grade)
    else:
        return redirect(url_for('login'))


#Apartado para saber la dieta del usuario
@app.route('/dieta')
def dieta():
    if logged_in_user:
        #comidas = api.get_food()
        #print(comidas)
        comida_usuario = api.get_food_user(correo_usuario)
        nombre_comida = ""
        ingredientes = ""
        descripcion = ""
        
        nombre_comidas_array = []
        ingredientes_array = []
        descripcion_array = []
        tiene_comidas = False

        if comida_usuario is not None:
            for i in range(len(comida_usuario)):
                if comida_usuario[i]['Borrada'] == 0:
                    nombre_comida = comida_usuario[i]['Nombre_comida']
                    ingredientes = comida_usuario[i]['Ingredientes']
                    descripcion = comida_usuario[i]['Descripcion']

                    nombre_comidas_array.append(nombre_comida)
                    ingredientes_array.append(ingredientes)
                    descripcion_array.append(descripcion)

                    tiene_comidas = True
            if not nombre_comida:
                tiene_comidas = False
        else:
            tiene_comidas = False

        return render_template('dieta.html', tiene_comidas = tiene_comidas, nombre_comidas_array = nombre_comidas_array, ingredientes_array = ingredientes_array, descripcion_array = descripcion_array)
    else:
        return redirect(url_for('login'))
    
class deleteDietForm(Form):
    correo_usuario = StringField('Correo del Usuario', [
        validators.DataRequired(),
        validators.Length(min=3, max=50)]
        )
    id_comida = StringField('ID de la Comida', [
        validators.DataRequired(),
        validators.Length(min=1, max=50)]
        )

#Apartado para borrar dietas a usuarios
@app.route('/delete_diet', methods=['GET', 'POST'])
def delete_diet():
    if logged_in_instructor:
        id_comidas = []
        nombre_comidas = []
        usuario_comidas = []
        todas_comidas = api.get_food()
        print(todas_comidas)
        for i in range(len(todas_comidas)):
            if todas_comidas[i]['Borrada'] == 0:
                id_comidas.append(int(todas_comidas[i]['Id_comida']))
                nombre_comidas.append(todas_comidas[i]['Nombre_comida'])
                usuario_comidas.append(todas_comidas[i]['Id_Cliente'])
        

        form = deleteDietForm(request.form)
        if request.method == 'POST' and form.validate():
            correo_usuario = form.correo_usuario.data
            id_comida = form.id_comida.data
            print(id_comida)
            if id_comida.isdigit():

                if correo_usuario.find('@') != -1:
                    existe_usuario = api.get_user(correo_usuario)
                    if existe_usuario is not None:
                        user_diet = api.get_food_id(int(id_comida))
                        if user_diet:
                            if user_diet[0]['Id_Cliente'] == correo_usuario:
                                borrar_comida = api.delete_food(int(id_comida))
                                if borrar_comida is not False:
                                    return redirect(url_for('home'))
                                else:
                                    error = 'El ID de la comida no existe, intenta con un id correcto'
                                    return render_template('delete_diet.html', form = form , error = error, id_comidas = id_comidas, nombre_comidas = nombre_comidas, usuario_comidas = usuario_comidas)
                            else:
                                error = 'No existe la comida para el usuario especificado'
                                return render_template('delete_diet.html', form = form , error = error, id_comidas = id_comidas, nombre_comidas = nombre_comidas, usuario_comidas = usuario_comidas)
                        else:
                            error = 'No existe la comida'
                            return render_template('delete_diet.html', form = form , error = error, id_comidas = id_comidas, nombre_comidas = nombre_comidas, usuario_comidas = usuario_comidas)
                
                    else: 
                        error = 'No existe el correo asociado a una cuenta'
                        return render_template('delete_diet.html', form = form , error = error, id_comidas = id_comidas, nombre_comidas = nombre_comidas, usuario_comidas = usuario_comidas)
                else:
                    error = 'No es un correo valido'
                    return render_template('delete_diet.html', form = form , error = error, id_comidas = id_comidas, nombre_comidas = nombre_comidas, usuario_comidas = usuario_comidas)
            else:
                error = 'Ingresa un ID que sea un numero'
                return render_template('delete_diet.html', form = form , error = error, id_comidas = id_comidas, nombre_comidas = nombre_comidas, usuario_comidas = usuario_comidas)
        return render_template('delete_diet.html', form = form, id_comidas = id_comidas, nombre_comidas = nombre_comidas, usuario_comidas = usuario_comidas)

    else:
        return redirect(url_for('login'))
    


@app.route('/clases')
def clases():
    if logged_in_user:
        todas_clases = api.get_classes()
        nombre_todas_clases = []
        id_todas_clases = []
        nombre_todos_instructores = []
        horarios_todas_clases = []
        aux_nombre_instructores = []
        aux_horarios = [] 

        for i in range(len(todas_clases)):
            #print('Debug')
            #print(todas_clases[i]['Cancelada'])
            if int(todas_clases[i]['Cancelada']) == 0:
                nombre_todas_clases.append(todas_clases[i]['Nombre'])
                id_todas_clases.append(todas_clases[i]['_id'])
                '''for x in range(len(todas_clases[i]['Instructores'])):
                    nombre_todos_instructores.append(todas_clases[i]['Instructores'][x])
                for p in range(len(todas_clases[i]['Horarios'])):
                    horarios_todas_clases.append(todas_clases[i]['Horarios'][p])'''
                #nombre_todos_instructores.append(todas_clases[i]['Instructores'])
                for x in range(len(todas_clases[i]['Instructores'])):
                    coach = api.get_one_instructor_id(todas_clases[i]['Instructores'][x])
                    nombre_coach = coach['Nombre_completo']
                    correo_coach = coach['email']
                    nombre_coach = ' ' + nombre_coach + ' (' + correo_coach + ') '
                    #print(nombre_coach)
                    aux_nombre_instructores.append(nombre_coach)
                #[x.encode('utf-8') for x in aux_nombre_instructores]
                #print(aux_nombre_instructores)
                #aux_nombre_instructores = [r.encode('utf-8') for r in aux_nombre_instructores]
                aux_nombre_instructores = ', '.join(map(str, aux_nombre_instructores))
                nombre_todos_instructores.append(aux_nombre_instructores)
                #print(nombre_todos_instructores)
                aux_nombre_instructores = []
                for p in range(len(todas_clases[i]['Horarios'])):
                    hors = todas_clases[i]['Horarios'][p]
                    hors = ' ' + hors + ' (' + str(p) + ') '
                    aux_horarios.append(hors)
                aux_horarios = ', '.join(map(str, aux_horarios))
                horarios_todas_clases.append(aux_horarios)
                aux_horarios= []


        clases_usuario = api.get_classes_user(correo_usuario)
        id_horario = ""
        id_instructor = 0
        id_clase = ""
        horario_clase = ""
        nombre_clase = ""
        nombre_instructor = ""
        ubicacion_clase = ""
        clases_aux = []
        nombre_clases = []
        nombre_instructores = []
        horario_clases = []
        ubicacion_clases = []
        
        if clases_usuario is not None:
            if clases_usuario[0]['Horario'] != -1:
                for i in range(len(clases_usuario)):
                    #print(clases_usuario[i])
                    #PUEDO BORRAR ESTO
                    id_horario = str(clases_usuario[i]['Horario'])
                    id_instructor = clases_usuario[i]['Instructor']
                    id_clase = clases_usuario[i]['Id_clase']

                    #Obtener la clase mediante el id
                    clase_info = api.get_one_class(id_clase)
                    print(clase_info)
                    #Guardando la informacion de las clases del usuario
                    horario_clase = clase_info['Horarios'][int(id_horario)] 
                    #Obtener instructor
                    id_instructor_str = clase_info['Instructores'][int(id_instructor)] 
                    info_instructor = api.get_one_instructor_id(id_instructor_str)
                    nombre_instructor = info_instructor['Nombre_completo']
                    nombre_clase = clase_info['Nombre']
                    #obtener salon (primero redefinir la estructura de la bd.tabla clase)

                    ubicacion_clase = clase_info['Ubicacion']

                    if int(clase_info['Cancelada']) == 0:
                        nombre_clases.append(nombre_clase)
                        nombre_instructores.append(nombre_instructor)
                        horario_clases.append(horario_clase)
                        ubicacion_clases.append(ubicacion_clase)
                        tiene_clases = True
                if len(nombre_clases) == 0:
                    tiene_clases = False
            else:
                tiene_clases = False
        else:
            tiene_clases = False

        return render_template('clases.html', nombre_todas_clases = nombre_todas_clases, id_todas_clases = id_todas_clases, nombre_todos_instructores = nombre_todos_instructores, horarios_todas_clases = horarios_todas_clases, tiene_clases = tiene_clases, nombre_clases = nombre_clases, nombre_instructores = nombre_instructores, horario_clases = horario_clases, ubicacion_clases = ubicacion_clases)
    
    else:
        return redirect(url_for('login'))
    

#Borrar un usuario
class deleteForm(Form):
    correo = StringField('Ingresa el correo del usuario:', [
        validators.DataRequired(),
        validators.Length(min=3, max=50)]
        )

#Borrar a un usuario en especifico
@app.route('/delete_users', methods=['GET', 'POST'])
def delete_users():
    if logged_in_instructor:
        usuarios = api.get_all_users()
        nombres_usuarios = []
        correos_usuarios = []
        id_usuarios = []
        direcciones_usuarios = []

        for i in range(len(usuarios)):
            id_usuarios.append(usuarios[i]['ID'])
            nombres_usuarios.append(usuarios[i]['Nombre_completo'])
            correos_usuarios.append(usuarios[i]['email'])
            direcciones_usuarios.append(usuarios[i]['Direccion'])
        
        form = deleteForm(request.form)
        if request.method == 'POST':
            email_user = form.correo.data
            #print(email_user)
            resultado_borrar = api.delete_user(email_user)
            if resultado_borrar == False:
                error = 'El correo que ingresaste no esta en la base de datos, vuelve a intentarlo'
                return render_template('delete_users.html', error = error, form = form, id_usuarios = id_usuarios, nombres_usuarios = nombres_usuarios, correos_usuarios = correos_usuarios, direcciones_usuarios = direcciones_usuarios)
            else:
                return redirect(url_for('home')) 
        return render_template('delete_users.html', form = form, id_usuarios = id_usuarios, nombres_usuarios = nombres_usuarios, correos_usuarios = correos_usuarios, direcciones_usuarios = direcciones_usuarios)
            
    else:
        return redirect(url_for('login'))

#Form para crear una clase
class claseForm(Form):
    nombre_clase = StringField('Nombre Clase:', [
        validators.DataRequired(),
        validators.Length(min=2, max=50)]
        )
    id_clase = StringField('Clase ID:', [
        validators.DataRequired(),
        validators.Length(min=1, max=500)]
        )
    horarios =  StringField('Horarios Clase:', [
        validators.DataRequired(),
        validators.Length(min=3, max=50)]
        )
    ubicacion =  StringField('Ubicacion Clase:', [
        validators.DataRequired(),
        validators.Length(min=3, max=50)]
        )

#Borrar una clase
class deleteClassForm(Form):
    id_clase = StringField('Ingresa el ID de la clase ha borrar:', [
        validators.DataRequired(),
        validators.Length(min=1, max=50)]
        )

#Borra una clase en especifico
@app.route('/delete_class', methods=['GET', 'POST'])
def delete_class():
    if logged_in_instructor:
        form = claseForm(request.form)
        
        todas_clases = api.get_classes()
        nombre_todas_clases = []
        id_todas_clases = []
        nombre_todos_instructores = []
        horarios_todas_clases = []
        aux_nombre_instructores = []
        aux_horarios = []

        for i in range(len(todas_clases)):
            if int(todas_clases[i]['Cancelada']) == 0:
                nombre_todas_clases.append(todas_clases[i]['Nombre'])
                id_todas_clases.append(todas_clases[i]['_id'])
                for x in range(len(todas_clases[i]['Instructores'])):
                    
                    coach = api.get_one_instructor_id(todas_clases[i]['Instructores'][x])
                    nombre_coach = coach['Nombre_completo']
                    nombre_coach = ' ' + nombre_coach + ' (' + str(x) + ') '
                    aux_nombre_instructores.append(nombre_coach.encode('utf-8'))

                aux_nombre_instructores = ', '.join(map(str, aux_nombre_instructores))
                nombre_todos_instructores.append(aux_nombre_instructores)
                aux_nombre_instructores = []

                for p in range(len(todas_clases[i]['Horarios'])):
                    hors = todas_clases[i]['Horarios'][p]
                    hors = ' ' + hors + ' (' + str(p) + ') '
                    aux_horarios.append(hors.encode('utf-8'))
                aux_horarios = ', '.join(map(str, aux_horarios))
                horarios_todas_clases.append(aux_horarios)
                aux_horarios= []

        form = deleteClassForm(request.form)
        if request.method == 'POST' and form.validate():
            id_clase = form.id_clase.data
            
            clase_info = api.get_one_class(id_clase)

            if clase_info is not False: #Existe la clase ha borrar
                if clase_info['Cancelada'] == 0:
                    resultado_borrar = api.delete_class(id_clase)
                    #print(resultado_borrar)
                    return redirect(url_for('home'))
                else:
                    error = 'Clase ya cancelada, inserta un id de las clases que aparecen en la lista'
                    return render_template('delete_class.html', form=form, error = error, nombre_todas_clases = nombre_todas_clases, horarios_todas_clases = horarios_todas_clases, nombre_todos_instructores = nombre_todos_instructores, id_todas_clases = id_todas_clases)

            else:
                error = 'No existe la clase con el id dado, checa bien la tabla'
                return render_template('delete_class.html', form=form, error = error, nombre_todas_clases = nombre_todas_clases, horarios_todas_clases = horarios_todas_clases, nombre_todos_instructores = nombre_todos_instructores, id_todas_clases = id_todas_clases)

        return render_template('delete_class.html', form = form, nombre_todas_clases = nombre_todas_clases, horarios_todas_clases = horarios_todas_clases, nombre_todos_instructores = nombre_todos_instructores, id_todas_clases = id_todas_clases)
    
    else:
        return redirect(url_for('login'))

    


if __name__ == "__main__":
    
    app.run(debug=True)