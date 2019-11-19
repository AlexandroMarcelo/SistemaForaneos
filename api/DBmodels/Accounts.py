import redis
from api import config

class Sessions(object):

    def __init__(self):
        if config.REDIS_PASSWORD:
            self.instance = redis.StrictRedis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                password=config.REDIS_PASSWORD)
        else:
            self.instance = redis.StrictRedis(
                host= config.REDIS_HOST,
                port=config.REDIS_PORT)


    def getUserPassword(self,user):
        """ Obtener un Password dado un correo """

        password = self.instance.get(user)

        if password is None: #Not found
            return False 
        else: 
            return password
