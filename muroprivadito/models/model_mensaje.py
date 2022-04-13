from flask import flash
from muroprivadito.config.mysqlconnection import connectToMySQL
import re

CONTENIDO_REGEX = re.compile(r'^(.){5,2000}$')

class Mensaje:
    name_db = "muro_privadito"
    def __init__(self,id,contenido,emisor_id,emisor,receptor_id,receptor,created_at):
        self.id = id
        self.contenido = contenido
        self.emisor_id = emisor_id
        self.emisor = emisor
        self.receptor_id = receptor_id
        self.receptor = receptor
        self.created_at = created_at

    @classmethod
    def sendMessage(cls,data):
        query = '''
                    INSERT INTO mensajes (contenido,emisor_id,receptor_id,created_at)
                    VALUES (%(contenido)s,%(emisor_id)s,%(receptor_id)s,now())
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,data)
        return resultado
    
    @classmethod
    def getMessagesXuser(cls,data):
        query = '''
                    select m.*, concat(u1.first_name," ",u1.last_name) as receptor,  concat(u2.first_name," ",u2.last_name) as emisor,
                    (CASE 
                    WHEN  (TIMESTAMPDIFF(YEAR,m.created_at,now()) > 0) THEN CONCAT(TIMESTAMPDIFF(YEAR,m.created_at,now()),' year(s) ago')
                    WHEN  (TIMESTAMPDIFF(MONTH,m.created_at,now()) > 0) THEN CONCAT(TIMESTAMPDIFF(MONTH,m.created_at,now()),' month(s) ago')
                    WHEN  (TIMESTAMPDIFF(DAY,m.created_at,now()) > 0) THEN CONCAT(TIMESTAMPDIFF(DAY,m.created_at,now()),' day(s) ago')
                    WHEN  (TIMESTAMPDIFF(HOUR,m.created_at,now()) > 0) THEN CONCAT(TIMESTAMPDIFF(HOUR,m.created_at,now()),' hour(s) ago')
                    WHEN  (TIMESTAMPDIFF(MINUTE,m.created_at,now()) > 0) THEN CONCAT(TIMESTAMPDIFF(MINUTE,m.created_at,now()),' minute(s) ago')
                    ELSE CONCAT(TIMESTAMPDIFF(SECOND,m.created_at,now()),' second(s) ago') END) AS created_at_diff
                    from mensajes m
                    inner join usuarios u1 on u1.id=m.receptor_id
                    inner join usuarios u2 on u2.id=m.emisor_id
                    where u1.id = %(id)s
                    order by m.created_at desc
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,data)
        mensajes = []
        for mensaje in resultado:
            aux = Mensaje(mensaje["id"],mensaje["contenido"],mensaje["emisor_id"],mensaje["emisor"],mensaje["receptor_id"],mensaje["receptor"],mensaje["created_at_diff"])
            mensajes.append(aux)
        return mensajes

    @classmethod
    def validateData(cls,data):
        is_valid = True
        if not CONTENIDO_REGEX.match(data["contenido"]):
            is_valid=False
            flash("El contenido del mensaje debe ser mayor de 5 caracteres","mensaje")
        return is_valid