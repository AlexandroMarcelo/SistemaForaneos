from pymongo import MongoClient
from bson import ObjectId
from api import config

class Grades(object):

    def __init__(self):
        client = MongoClient(config.MONGO_URI)
        db = client.ITESMSystem
        self.user_collection = db.grades
        self.teacher_collection = db.instructors
        self.student_collection = db.students

#STUDENTS
    def findStudent(self, mail):
        """
        Get a student given his mail
        """
        student = self.student_collection.find_one({'mail': mail})
        
        # Parsing the ObjectID to make it readable
        if student is not None:
            student['_id'] = str(student['_id'])

        return student
    
    def findStudentName(self, mail):
        """
        Get the name of a student given his mail
        """
        student = self.findStudent(mail)
        student_name = "ERROR"
        # Parsing the ObjectID to make it readable
        if student is not None:
            student_name = str(student['name'])

        return student_name


#USERS GRADES
    def findGrades(self):
        """
        Get the grades of all users
        """
        grades = self.user_collection.find()
        all_grades = []

        for grade in grades:
            # Parsing the ObjectID to make it readable
            grade['_id'] = str(grade['_id']) 
            all_grades.append(grade)

        return all_grades


    def findUserGrades(self, mail, current_week):
        """
        Get the grades of a given user
        """
        grades = self.findGrades()
        
        user_grades = []
        for grade in grades:
            if grade['studentID'] == mail and grade['week'] == current_week:
                user_grades.append(grade)
        return user_grades

    def findTotalWeeks(self):
        """
        Get the number of the total weeks
        """
        grades = self.findGrades()
        
        total_weeks = 0
        for grade in grades:
            if int(str(grade['week'])) > total_weeks:
                total_weeks = total_weeks + 1
        return total_weeks

#TEACHER GRADES
    def findTeacher(self, mail):
        """
        Get a teacher given his mail
        """
        teacher = self.teacher_collection.find_one({'mail': mail})
        
        # Parsing the ObjectID to make it readable
        if teacher is not None:
            teacher['_id'] = str(teacher['_id'])

        return teacher

    def findTeacherName(self, mail):
        """
        Get the name of the teacher given his mail
        """
        teacher = self.findTeacher(mail)
        teacher_name = "Teacher not found"
        # Parsing the ObjectID to make it readable
        if teacher is not None:
            teacher_name = teacher['name']

        return teacher_name

    def findStudentsGrades(self, current_class, week):
        """
        Get the grades of all students enrolled to a particular class
        """
        grades = self.findGrades()
        users_grades = []
        for grade in grades:
            if grade['class'] == current_class and grade['week'] == week:
                users_grades.append(grade)

        return users_grades

    def findClassesTeacher(self, mail):
        """
        Get the classes of the teacher
        """
        all_classes = self.findGrades()
        classes = []
        for classs in all_classes:
            if classs['class'] not in classes:
                classes.append(classs['class'])

        return classes

    def insertGrades(self, document):
        """
        Insert the grades of a new week
        """
        cursor = self.user_collection.insert_one(document)

        print(cursor)
        print(cursor.inserted_id)
        if cursor.inserted_id is not None:
            return True
        else:
            return False

    def updateGrades(self, document):
        """
        Updates the grades of the students
        """
        student = self.findStudent(document['studentID'])
        if student is not None: #if exist
            print("asdsas")
            print(document)
            #update_student = self.student_collection.update_one({'studentID': document['studentID'], "week" : document['week'], "class" : document['class']}, {'$set' : {'academic':document['academic'], 'teamWork':document['teamWork'], 'communication':document['communication']}}, upsert = True) 
            delete_student = self.user_collection.delete_one({"class" : document['class'], "week" : document['week'], 'studentID': document['studentID']})
            print(delete_student)
            if delete_student.deleted_count == 1:
                cursor = self.user_collection.insert_one(document)
                return cursor #deleted successfully
            else:
                return False
        else: #student no exist
            return False
