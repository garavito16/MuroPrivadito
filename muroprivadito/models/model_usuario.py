from flask import flash
from muroprivadito.config.mysqlconnection import connectToMySQL
import re

NAMES_REGEX = re.compile(r'^[A-Z][a-zA-Z ]{1,80}$')
PASSWORD_REGEX = re.compile(r'^(.)*(?=\w*\d)(?=\w*[A-Z])\S{8,16}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    name_db = "muro_privadito"
    def __init__(self,id,nombres,apellidos,email,password,created_at,mensajes_enviados):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.email = email
        self.password = password
        self.created_at = created_at
        self.mensajes_enviados = mensajes_enviados

    @classmethod
    def addUser(cls,user):
        query = '''
                    INSERT INTO usuarios (first_name,last_name,password,email,created_at)
                    VALUES (%(first_name)s,%(last_name)s,%(password)s,%(email)s,now())
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,user)
        return resultado

    @classmethod
    def userXLogin(cls,user):
        query = '''
                    SELECT us.*, COUNT(m.id) as mensajes_enviados FROM usuarios us
                    LEFT JOIN mensajes m ON us.id = m.emisor_id
                    WHERE us.email = %(email)s
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,user)
        if(len(resultado) > 0):
            user = User(resultado[0]["id"],resultado[0]["first_name"],resultado[0]["last_name"],resultado[0]["email"],resultado[0]["password"],resultado[0]["created_at"],resultado[0]["mensajes_enviados"])
            return user
        else:
            return None
    
    @classmethod
    def listOtherUsers(cls,user):
        query = '''
                    SELECT * FROM usuarios WHERE id != %(id)s
                    ORDER BY first_name ASC, last_name ASC
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,user)
        print(user)
        usuarios = []
        for usuario in resultado:
            user = User(usuario["id"],usuario["first_name"],usuario["last_name"],usuario["email"],usuario["password"],usuario["created_at"],0)
            usuarios.append(user)
        return usuarios

    @classmethod
    def verifyData(cls,user):
        is_valid = True
        if not NAMES_REGEX.match(user["first_name"]):
            is_valid = False
            flash("First Name debe tener 2 caracteres como minimo. La primer letra debe ser mayuscula","registro")
        if not NAMES_REGEX.match(user["last_name"]):
            is_valid = False
            flash("Last name debe tener 2 caracteres como minimo. La primera letra debe ser mayusccula","registro")
        if not EMAIL_REGEX.match(user["email"]):
            is_valid = False
            flash("Email no es correcto","registro")
        if not PASSWORD_REGEX.match(user["password"]):
            is_valid = False
            flash("Password no es correcta. Debe tener entre 8 y 16 caracteres y ademas debe incluir una letra y un numero","registro")
        if user["password"] != user["confirm_password"]:
            is_valid = False
            flash("El password debe ser igual a la confirmación de password","registro")
        return is_valid

    @classmethod
    def verifyDataLogin(cls,user):
        is_valid = True
        if not EMAIL_REGEX.match(user["email"]):
            is_valid = False
            flash("Email no es correcto","login")
        if not PASSWORD_REGEX.match(user["password"]):
            is_valid = False
            flash("Password no es correcta","login")
        return is_valid