# -*- coding: utf-8 -*-
from flask import Flask,  jsonify, render_template, flash, redirect, url_for, session, request, logging  #render_template: para recargar la pagina

from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from csvvalidator import *
#from DBmodels import Gimnasio
#import jinja2
import os, sys, getopt, pprint
import pandas as pd
import json
import csv
sys.path.insert(0, os.path.abspath(".."))


#from api.DBmodels import Gimnasio
from api import GradesAPI

app = Flask(__name__)
app.secret_key='12345'
UPLOAD_FOLDER = './documentos/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt','csv'])

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
        password_redis = apiGrades.get_password_user(email)

        #print(input_password)
        
        #print(password_redis)
        if domain == 'tec.mx': #for teachers
            if password_redis is not False: #Not found
                if sha256_crypt.verify(input_password, password_redis):
                #if True:
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
                if sha256_crypt.verify(input_password, password_redis):
                #Aqui
                #if True:
                    app.logger.info('VALIDO')
                    session['logged_in'] = True
                    session['nombre'] = nombre_usuario
                    global logged_in_user
                    logged_in_user = True
                    return redirect(url_for('home'))
                
                else:
                    error = 'Usuario no encontrado'
                    app.logger.info('NO VALIDO')
                    return render_template('login.html', error=error)
                
    
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
        session['week'] = current_week
        session['selected_class'] = True
        selected_class = "Programming"
        if request.args.get('selected_class', None) == None:
            selected_class = session['class']
        else: 
            selected_class = request.args.get('selected_class', None)
            session['class'] = request.args.get('selected_class', None)
        
        users_grades = apiGrades.get_students_grades(selected_class, current_week)
        total_weeks = apiGrades.get_total_weeks_class(session['class'])
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
        
        #initializing errors flags
        updated_correctly = False
        updated_error_db = False
        updated_student_no_enrolled = False
        updated_student_no_exist = False

        path_csv = ''
        ### Upload function
        if request.method == 'POST':
            if request.form['submit_button'] == 'Submit Grade':
                # check if the post request has the file part
                if 'file' not in request.files:
                    flash('No file part')
                file = request.files['file']
                if file.filename == '':
                    flash('Please add a valid file to upload grades to week: ' + str(total_weeks+1))
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    path_csv = app.config['UPLOAD_FOLDER'] + filename
                    csvfile = open(path_csv, 'r')
                    csvfile2 = open(path_csv, 'r')
                    reader = csv.DictReader( csvfile )
                    reader2 = csv.DictReader( csvfile2 )
                    header= ['studentID', 'academic', 'teamWork', 'communication']
                    field_names = ('studentID', 'academic', 'teamWork', 'communication')
                    validator = CSVValidator(field_names)
                    # basic header and record length checks
                    validator.add_header_check('EX1', 'bad header')
                    problems = validator.validate(reader)

                    if bool(problems):
                        if problems[0]['code'] == 'EX1':
                            flash('ERROR: Document is invalid, please check the header, you should have studentId,academic,teamWork,communication, in that format')
                    else:
                        flash('File successfully uploaded')
                        for each in reader2:#iteration to read every row of the document
                            row={}
                            row['class'] = session['class']
                            row['week'] = total_weeks + 1
                            #count for error control
                            cont = 0

                            for field in header:
                                    row[field]=each[field]
                            
                            try:#catching error in case the format of the document is wrong
                                academic = int(row['academic'])
                                teamWork = int(row['teamWork'])
                                communication = int(row['communication'])
                               
                                if academic in range(100):
                                    cont+=1
                            
                                else:
                                    flash('Error found in an academic field, please check the document and try again')

                                if teamWork in range(100):
                                    cont+=1
        
                                else:
                                    flash('Error found in an team work field, please check the document and try again') 

                                if communication in range(100):
                                    cont+=1
                                    
                                else:
                                    print('Error, communication is wrong')
                                    flash('Error found in an communication field, please check the document and try again')

                                if cont == 3:
                                    insert_grades = apiGrades.insert_grades(row)
                                    if insert_grades is False:
                                        flash("Error in the DB, please check the selected file and upload it agin.")
                                    else:
                                        flash("Grades inserted correctly")

                                elif cont != 3:
                                    flash('File had an error and could not be uploaded, try again!')

                            except ValueError:
                                pass                             
                                flash("Error in the file, please check that every field has a number between 0 and 100 and the ID is valid.")

                    os.remove(path_csv)
                    
                else:
                    if file.filename == '':
                        flash('Allowed file types are csv')
                    if path_csv is not '':
                        os.remove(path_csv)
                ### Upload funtion end


            elif request.form['submit_button'] == 'Update Grade':
                print('updating')
                ### Update funtion begin
                # check if the post request has the file part
                if 'file' not in request.files:
                    flash('No file part')
                file = request.files['file']
                if file.filename == '':
                    flash('Please add a valid file to upload grades to week: ' + str(total_weeks+1))
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    path_csv = app.config['UPLOAD_FOLDER'] + filename
                    csvfile = open(path_csv, 'r')
                    csvfile2 = open(path_csv, 'r')
                    reader = csv.DictReader( csvfile )
                    reader2 = csv.DictReader( csvfile2 )
                    header= ['studentID', 'academic', 'teamWork', 'communication']
                    field_names = ('studentID', 'academic', 'teamWork', 'communication')
                    validator = CSVValidator(field_names)
                    # basic header and record length checks
                    validator.add_header_check('EX1', 'bad header')
                    problems = validator.validate(reader)
                    
                    if bool(problems):
                        if problems[0]['code'] == 'EX1':
                            flash('ERROR: Document is invalid, please check that it has the correct format!!')
                    else:
                        flash('File successfully uploaded')
                        for each in reader2:
                            row={}
                            row['class'] = session['class']
                            row['week'] = session['week']
                            for field in header:
                                    row[field]=each[field]
                            print(row)
                            update_grades = apiGrades.update_grades(row)
                            if update_grades == -1:
                                updated_error_db+=1
                                updated_correctly = False
                            elif update_grades == -2:
                                updated_student_no_enrolled+=1
                                updated_correctly = False
                            elif update_grades == -3:
                                updated_student_no_exist+=1
                                updated_correctly = False
                        if updated_correctly:
                            flash("Everything was uploaded correctly. Grades updated")
                        if updated_error_db >= 1:
                            flash("Error in the DB, please check the selected file and upload it again.")
                        if updated_student_no_enrolled >= 1:
                            flash(str(updated_student_no_enrolled) + " students not enrolled.")
                        if updated_student_no_exist >= 1:
                            flash(str(updated_student_no_exist) + "The student does not exist")
                    os.remove(path_csv)
                else:
                    if file.filename == '':
                        flash('Allowed file types are csv')
                    if path_csv is not '':
                        os.remove(path_csv)
                ### Upload funtion end
            elif request.form['submit_button'] == 'View Week':
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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    
    app.run(debug=True)