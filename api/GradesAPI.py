from flask import request, url_for, jsonify
from flask_api import FlaskAPI, status, exceptions
from api.DBmodels import Grades, Accounts
from datetime import datetime
from bson import ObjectId

from flask import Flask, jsonify,request,make_response,url_for,redirect
from json import dumps
import requests

api_url = 'http://apistudentexchange.azurewebsites.net/'
#api_url = 'http://localhost:5050/'

class GradesAPI(object):
#AUTH
    def get_password_user(self, email):
        service = 'get_user_password/'
        student = email
        data = str(api_url+service+student)
        try:
            r = requests.get(data)
        except:
            return "API ERROR"
        print(r.status_code, r.reason, r.text)
        if r.status_code >= 200 and r.status_code < 400:
            return r.text
        else:
            return "API ERROR"
        """
        mongodb = Accounts.Sessions()
        grades = mongodb.getUserPassword(email)
        return grades"""
        
#USERS
    def get_name_student(self,mail):
        service = 'student_name/'
        student = mail
        data = str(api_url+service+student)
        try:
            r = requests.get(data)
        except:
            return "API ERROR"
        if r.status_code >= 200 and r.status_code < 400:
            return r.text
        else:
            return "API ERROR"
        """
        mongodb = Grades.Grades()
        grades = mongodb.findStudentName(mail)
        return grades
        """

#USERS GRADES
    def get_grades(self):
        mongodb = Grades.Grades()
        grades = mongodb.findGrades()
        return grades
    
    def get_user_grades(self, mail, current_week):
        service = 'get_user_grades/'
        student = mail
        current_week = current_week
        current_week_api = str(current_week)
        current_week_api = '/'+current_week_api
        data = str(api_url+service+student+current_week_api)
        try:
            r = requests.get(data)
        except:
            return "API ERROR"
        if r.status_code >= 200 and r.status_code < 400:
            return r.text
        else:
            return "API ERROR"
        """
        mongodb = Grades.Grades()
        user_grades = mongodb.findUserGrades(mail, current_week)
        return user_grades
        """
    def get_total_weeks(self):
        service = 'get_total_weeks'
        data = str(api_url+service)
        try:
            r = requests.get(data)
        except:
            return "API ERROR"
        if r.status_code >= 200 and r.status_code < 400:
            return r.text
        else:
            return "API ERROR"
        """
        mongodb = Grades.Grades()
        total_weeks = mongodb.findTotalWeeks()
        return total_weeks
        """

    def get_total_weeks_class(self, class_name):
        service = 'get_total_weeks_class'
        data = str(api_url+service+"/"+class_name)
        try:
            r = requests.get(data)
        except:
            return "API ERROR"
        if r.status_code >= 200 and r.status_code < 400:
            return r.text
        else:
            return "API ERROR"
        """
        mongodb = Grades.Grades()
        total_weeks = mongodb.findTotalWeeksClass(class_name)
        return total_weeks
        """

    def insert_grades(self, document):
        service = 'insert_grades'
        #data_json = {'class': 'Programming','week':1, 'studentID':'A01021383@itesm.mx','academic':'10','teamWork':'80', 'communication':'90'}
        api_url_test =  str(api_url+service)
        try:
            r = requests.post(url=api_url_test, json=document)
        except:
            return "API ERROR"
        if r.status_code >= 200 and r.status_code < 400:
            return r.text
        else:
            return "API ERROR"
        #print(r.status_code, r.reason, r.text)
        #return r.text
        """mongodb = Grades.Grades()
        inserted_grades = mongodb.insertGrades(document)
        return inserted_grades"""

    def update_grades(self, document):
        service = 'update_grades'
        api_url_test =  str(api_url+service)
        try:
            r = requests.post(url=api_url_test, json=document)
        except:
            return "API ERROR"
        if r.status_code >= 200 and r.status_code < 400:
            return r.text
        else:
            return "API ERROR"
        """mongodb = Grades.Grades()
        updated_grades = mongodb.updateGrades(document)
        return updated_grades"""

#TEACHERS
    def get_teacher_name(self, mail):
        service = 'teacher_name/'
        teacher = mail
        data = str(api_url+service+teacher)
        
        try:
            r = requests.get(data)
        except:
            return "API ERROR"
        #print(r.json)
        #print(r.status_code, r.reason, r.text)
        if r.status_code >= 200 and r.status_code < 400:
            return r.text
        else:
            return "API ERROR"

    def get_students_grades(self, current_class, week):
        service = 'get_students_grades/'
        class_name = current_class
        current_week = week
        current_week_api = str(current_week)
        current_week_api = '/'+current_week_api
        data = str(api_url+service+class_name+current_week_api)
        try:
            r = requests.get(data)
        except:
            return "API ERROR"
        if r.status_code >= 200 and r.status_code < 400:
            return r.text
        else:
            return "API ERROR"
        """
        mongodb = Grades.Grades()
        teacher_name = mongodb.findStudentsGrades(current_class, week)
        return teacher_name
        """

    def get_classes_teacher(self, mail):
        service = 'get_classes_teacher/'
        data = str(api_url+service+mail)
        try:
            r = requests.get(data)
        except:
            return "API ERROR"
        if r.status_code >= 200 and r.status_code < 400:
            return r.text
        else:
            return "API ERROR"
        """
        mongodb = Grades.Grades()
        teacher_name = mongodb.findClassesTeacher(mail)
        return teacher_name
        """
    