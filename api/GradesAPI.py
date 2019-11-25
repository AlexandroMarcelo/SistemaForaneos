from flask import request, url_for, jsonify
from flask_api import FlaskAPI, status, exceptions
from api.DBmodels import Grades
from datetime import datetime
from bson import ObjectId
import json
import random

class GradesAPI(object):
#USERS
    def get_name_student(sel,mail):
        mongodb = Grades.Grades()
        grades = mongodb.findStudentName(mail)
        return grades

#USERS GRADES
    def get_grades(self):
        mongodb = Grades.Grades()
        grades = mongodb.findGrades()
        return grades
    
    def get_user_grades(self, mail, current_week):
        mongodb = Grades.Grades()
        user_grades = mongodb.findUserGrades(mail, current_week)
        return user_grades

    def get_total_weeks(self):
        mongodb = Grades.Grades()
        total_weeks = mongodb.findTotalWeeks()
        return total_weeks
    
    def insert_grades(self, document):
        mongodb = Grades.Grades()
        inserted_grades = mongodb.insertGrades(document)
        return inserted_grades

    def update_grades(self, document):
        mongodb = Grades.Grades()
        updated_grades = mongodb.updateGrades(document)
        return updated_grades

#TEACHERS
    def get_teacher_name(self, mail):
        mongodb = Grades.Grades()
        teacher_name = mongodb.findTeacherName(mail)
        return teacher_name

    def get_students_grades(self, current_class, week):
        mongodb = Grades.Grades()
        teacher_name = mongodb.findStudentsGrades(current_class, week)
        return teacher_name

    def get_classes_teacher(self, mail):
        mongodb = Grades.Grades()
        teacher_name = mongodb.findClassesTeacher(mail)
        return teacher_name
    