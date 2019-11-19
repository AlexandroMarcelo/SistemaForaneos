from pymongo import MongoClient
from bson import ObjectId
from api import config

class Gimnasio(object):

    def __init__(self):
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        self.collection = db.clientes

#Usuarios
    def find(self):
        """
        Obtener todos los usuarios
        """
        cursor = self.collection.find()

        usuarios = []

        for usuario in cursor:
            # Se adiciono para poder manejar ObjectID
            usuario['_id'] = str(usuario['_id']) 
            usuarios.append(usuario)

        return usuarios

    def findOne(self, mail):
        """
        Obtener un usuario dado un correo
        """
        usuario = self.collection.find_one({'email': mail})
        # Se adiciono para poder manejar ObjectID
        if usuario is not None:
            usuario['email'] = str(usuario['email'])
            

        return usuario

    def getNumberOfUsers(self):
        """
        Actualizar un ususario
        """
        result = self.collection.count()

        return result

#CLASES
    def findClasses(self):
        """
        Obtener todas las clases
        """
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.clases
        
        clases = collection.find()
        all_classes = []

        for clase in clases:
            # Se adiciono para poder manejar ObjectID
            clase['_id'] = str(clase['_id']) 
            all_classes.append(clase)

        return all_classes

    def findOneClass(self, id):
        """
        Obtener una clase  dado su id
        """
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.clases
        
        clase = collection.find_one({'_id': id})
        if clase is not None:
            return clase
        else:
            return False

    def deleteClass(self, id_clase):
        '''
        Borrar una clase
        '''
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.clases

        result = collection.update({'_id':id_clase, "Cancelada":0}, {'$set': {'Cancelada': 1}})        
        return result

#DIETAS
    def findFood(self):
        '''
        Obtener todas las comidas
        '''
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.dietas
        
        cursor = collection.find()

        dietas = []

        for dieta in cursor:
            # Se adiciono para poder manejar ObjectID
            dieta['_id'] = str(dieta['_id']) 
            dietas.append(dieta)

        return dietas

    #obtener dietas de un usuario
    def findFoodUser(self, email):
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.dietas
        
        #cursor = collection.replace_one({'Id_Cliente': 'U000001'}, {'Id_comida': 0, 'Nombre_comida': 'Pollo ahumado', 'Id_Cliente': 'act@gmail.com', 'Ingredientes': '100 gr pollo, 100 gr de brocoli, 100 gr papa', 'Descripcion': 'Preparala sin aceite y cocinala lentamente al fuego, el brocoli cocinalo al vapor, y la papa al horno'})

        cursor = collection.find({'Id_Cliente': email})
        dietas = []
        
        for dieta in cursor:
            # Se adiciono para poder manejar ObjectID
            dieta['_id'] = str(dieta['_id']) 
            dietas.append(dieta)
        
        return dietas

    def findFoodID(self, id):
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.dietas

        cursor = collection.find({'Id_comida': id})
        dietas = []
        for dieta in cursor:
            # Se adiciono para poder manejar ObjectID
            dieta['_id'] = str(dieta['_id']) 
            dietas.append(dieta)
        
        return dietas

#INSTRUCTORES
    def findInstructors(self):
        '''
        Obtener a todos los instructores
        '''
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.instructores
        
        #cursor = collection.replace_one({'Id_Cliente': 'U000001'}, {'Id_comida': 0, 'Nombre_comida': 'Pollo ahumado', 'Id_Cliente': 'act@gmail.com', 'Ingredientes': '100 gr pollo, 100 gr de brocoli, 100 gr papa', 'Descripcion': 'Preparala sin aceite y cocinala lentamente al fuego, el brocoli cocinalo al vapor, y la papa al horno'})

        cursor = collection.find()
    
        instructores = []
        
        for instructor in cursor:
            # Se adiciono para poder manejar ObjectID
            instructor['_id'] = str(instructor['_id']) 
            instructores.append(instructor)
        
        return instructores

    def findOneInstructorId(self, id):
        '''
        Encontrar a un instructor dado su id
        '''
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.instructores
        
        cursor = collection.find_one({'ID_Instructor': id})
        
        return cursor
    
    def findOneInstructorEmail(self, correo):
        '''
        Encontrar a un instructor dado su correo
        '''
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.instructores
        
        cursor = collection.find_one({'email': correo})
        
        return cursor

    
    def getNumberOfInstructors(self):
        '''
        Obtener el numero de instructores que hay en la base de datos
        '''

        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.instructores

        count = collection.count()

        return count