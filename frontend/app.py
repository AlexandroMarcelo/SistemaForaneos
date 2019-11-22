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
        #print(password)
        #password_redis = api.get_password_user(email)

        password_redis = True
        #print(input_password)
        
        #print(password_redis)
        if domain == 'tec.mx': #for teachers
            if password_redis is not False: #Not found
                #if sha256_crypt.verify(input_password, password_redis):
                if True:
                    teacher_name = apiGrades.get_teacher_name(email)
                    session['instructor'] = True
                    session['nombre'] = str(teacher_name)
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
            nombre_usuario = apiGrades.get_name_student(email)
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
    
    #print(api.get_all_users())
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

#Where the student can view their grades of each class
@app.route('/user_grades', methods=['GET', 'POST'])
def user_grades():
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
        return render_template('user_grades.html', current_week=current_week, weeks=weeks, class_name=class_name, academic_grade=academic_grade, team_work_grade=team_work_grade, communication_skill_grade=communication_skill_grade)
    else:
        return redirect(url_for('login'))




#Borrar a un usuario en especifico
@app.route('/instructor_grades', methods=['GET', 'POST'])
def instructor_grades():
    if logged_in_instructor:
        #Just to get the total of weeks for the dropdown 
        current_week = request.form.get('current_week')
        if current_week == None:
            current_week = 0
        current_week = int(str(current_week))
        session['selected_class'] = True
        selected_class = "Programming"
        if request.args.get('selected_class', None) == None:
            selected_class = session['class']
        else: 
            selected_class = request.args.get('selected_class', None)
            session['class'] = request.args.get('selected_class', None)
        
        users_grades = apiGrades.get_students_grades(selected_class, current_week)
        total_weeks = apiGrades.get_total_weeks()
        weeks = []
        helper_weeks = 1
        while helper_weeks <= total_weeks:
            weeks.append(helper_weeks)
            helper_weeks = helper_weeks + 1

        #Filling the lists for the grades for the user
        student_id = []
        class_name = []
        academic_grade = []
        team_work_grade = []
        communication_skill_grade = []
        for grades in users_grades:
            student_id.append(grades['studentID'])
            academic_grade.append(grades['academic'])
            team_work_grade.append(grades['teamWork'])
            communication_skill_grade.append(grades['communication'])
        return render_template('instructor_grades.html', current_week=current_week, current_class=selected_class, student_id=student_id, weeks=weeks, academic_grade=academic_grade, team_work_grade=team_work_grade, communication_skill_grade=communication_skill_grade)    
    else:
        return redirect(url_for('login'))

#Borrar a un usuario en especifico
@app.route('/classes', methods=['GET', 'POST'])
def classes():
    if logged_in_instructor:
        classes = apiGrades.get_classes_teacher(correo_usuario)
        
        return render_template('classes.html', class_name=classes)    
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