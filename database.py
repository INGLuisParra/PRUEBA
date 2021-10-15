import sqlite3

class database:
    db_name = 'database.db'
    def __init__(self):
        self.cnn= sqlite3.connect(self.db_name)

    def __str__(self):
        datos =self.consulta_tareas()
        aux = ''
        for row in datos:
            aux = aux + str(row) + '\n'
        return aux

    def consulta_tareas(self):
        cur = self.cnn.cursor()
        cur.execute('SELECT * FROM TASK')
        datos = cur.fetchall()
        cur.close()
        return datos

    def buscar_tarea(self, TASKID):
        cur = self.cnn.cursor()
        sql = 'SELECT * FROM TASK WHERE TASKID = {}'.format(TASKID)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()
        return datos

    def insertar_datos(self,taskname, taskdescription, taskactive, taskdate):
        cur = self.cnn.cursor()
        sql = '''INSERT INTO TASK (taskname, taskdescription, taskactive, taskdate) 
                 VALUES ('{}', '{}', '{}', '{}')'''.format(taskname, taskdescription, taskactive, taskdate)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n

    def eliminar_tarea(self,TASKID):
        cur = self.cnn.cursor()
        sql = '''DELETE  FROM TASK WHERE TASKID = {}'''.format(TASKID)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n

    def modificar_tarea(self, taskid, TASKNAME, TASKDESCRIPTION, TASKACTIVE, TASKDATE):
        cur = self.cnn.cursor()
        sql = '''UPDATE TASK SET TASKNAME='{}', TASKDESCRIPTION='{}', TASKACTIVE='{}', TASKDATE='{}' 
        WHERE taskid={}'''.format(TASKNAME, TASKDESCRIPTION, TASKACTIVE,TASKDATE,taskid)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()

    def hecho(self, taskid, TASKACTIVE):
        cur = self.cnn.cursor()
        sql = '''UPDATE TASK SET  TASKACTIVE='{}' WHERE taskid={}'''.format(TASKACTIVE, taskid)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()