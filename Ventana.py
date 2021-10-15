from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import date
from datetime import datetime
from database import *

class Ventana(Frame):
    tareas = database()
    now = datetime.now()

    def __init__(self, master=None):
        super().__init__(master, width=720, height=260)
        self.master = master
        self.pack()
        self.create_widgets()
        self.llenartabla()
        self.habilitarceldas('disabled')
        self.habilitarbtguardar('normal')
        self.hablititarbtop('normal')
        self.taskid = -1
        self.estado = 1

    def habilitarceldas(self,estado):
        self.txtName.configure(state=estado)
        self.txtDescription.configure(state=estado)

    def hablititarbtop(self,estado):
        self.btNuevo.configure(state=estado)
        self.btModificar.configure(state=estado)
        self.btBorrar.configure(state=estado)
        self.btInfo.configure(state=estado)
        self.btHecho.configure(state=estado)


    def habilitarbtguardar(self,estado):
        self.btGuardar.configure(state=estado)
        self.btCancelar.configure(state=estado)

    def llenartabla(self):
        datos = self.tareas.consulta_tareas()

        for row in datos:
            self.grid.insert('', END, text=row[0], values=(row[1], row[2], row[3], row[4]))

    def limpiar(self):
        self.txtName.delete(0,END)
        self.txtDescription.delete(0, END)

    def fNuevo(self):
        self.habilitarceldas('normal')
        self.hablititarbtop('disabled')
        self.habilitarbtguardar('normal')
        self.limpiar()
        self.txtName.focus()


    def fModificar(self):
        selected = self.grid.focus()
        clave = self.grid.item(selected, 'text')
        if clave == '':
            messagebox.showwarning('borrar', 'Debes escoger una tarea')
        else:

            self.taskid = clave
            self.habilitarceldas('normal')
            valores = self.grid.item(selected, 'values')
            self.limpiar()

            self.txtName.insert(0,valores[0])
            self.txtDescription.insert(0,valores[1])

            self.hablititarbtop('disabled')
            self.habilitarbtguardar('normal')
            self.txtName.focus()



    def fBorar(self):
        selected = self.grid.focus()
        clave = self.grid.item(selected,'text')
        if clave == '':
            messagebox.showwarning('borrar','Debes escoger una tarea')

        else:
            valores = self.grid.item(selected,'values')
            data = str(clave) + ", " + valores[0]
            r = messagebox.askquestion('borrar',"¿esta seguro de eliminar esta tarea?\n" + data)
            if r == messagebox.YES:
                n = self.tareas.eliminar_tarea(clave)

                if n == 1:
                    messagebox.showinfo('borrar', 'tarea eliminada')
                    self.limpiargrid()
                    self.llenartabla()
                else:
                    messagebox.showinfo('borrar', 'no se pudo eliminar')

    def fHecho(self):
        selected = self.grid.focus()
        clave = self.grid.item(selected, 'text')
        if clave == '':
            messagebox.showwarning('borrar', 'Debes escoger una tarea')
        else:
            self.taskid = clave
            self.tareas.hecho(self.taskid,0)
        self.limpiargrid()
        self.llenartabla()

    def fGuardar(self):
        if self.taskid == -1:
            self.tareas.insertar_datos(self.txtName.get(),self.txtDescription.get(),self.estado,self.now.date())


        else:
            self.tareas.modificar_tarea(self.taskid,self.txtName.get(),self.txtDescription.get(),self.estado,self.now.date())
            self.id = -1

        self.limpiargrid()
        self.llenartabla()
        self.limpiar()
        self.habilitarbtguardar('disabled')
        self.hablititarbtop('normal')
        self.habilitarceldas('disabled')

    def limpiargrid(self):
        for item in self.grid.get_children():
            self.grid.delete(item)

    def fCancelar(self):
        r = messagebox.askquestion('Cancelar', "¿esta seguro de cancelar esta tarea?")
        if r == messagebox.YES:
            self.limpiar()
            self.habilitarbtguardar('disabled')
            self.hablititarbtop('normal')
            self.habilitarceldas('normal')

    def finfo(self):
        selected = self.grid.focus()
        clave = self.grid.item(selected, 'text')
        if clave == '':
            messagebox.showwarning('borrar', 'Debes escoger una tarea')
        else:
            self.taskid = clave
            valores = self.grid.item(selected, 'values')
            messagebox.showinfo('Descrpción', valores[1])


    def create_widgets(self):
        now = datetime.now()
        #Frame de botones
        frame1 = Frame(self, bg='#43444f')
        frame1.place(x=0,y=0,width=100, height=260)

        self.btNuevo = Button(frame1, text='Nuevo', command=self.fNuevo, bg='yellow', fg='black')
        self.btNuevo.place(x=10,y=10,width=80,height=30)

        self.btModificar = Button(frame1, text='Modificar', command=self.fModificar, bg='yellow', fg='black')
        self.btModificar.place(x=10, y=50, width=80, height=30)

        self.btBorrar = Button(frame1, text='Borrar', command=self.fBorar, bg='yellow', fg='black')
        self.btBorrar.place(x=10, y=90, width=80, height=30)

        self.btHecho = Button(frame1, text='Hecho', command=self.fHecho, bg='yellow', fg='black')
        self.btHecho.place(x=10, y=130, width=80, height=30)

        self.btInfo = Button(frame1, text='Info', command=self.finfo, bg='yellow', fg='black')
        self.btInfo.place(x=10, y=170, width=80, height=30)

        #Frame de entradas
        frame2 = Frame(self, bg='#9c2d2d')
        frame2.place(x=101, y=0, width=150, height=260)

        lbl1 = Label(frame2,text='taskName',bg='#9c2d2d')
        lbl1.place(x=3,y=5)
        self.txtName = Entry(frame2)
        self.txtName.place(x=3, y=25, width=140,height=20)

        lbl2 = Label(frame2, text='taskDescription', bg='#9c2d2d')
        lbl2.place(x=3, y=55)
        self.txtDescription = Entry(frame2)
        self.txtDescription.place(x=3, y=75, width=140, height=20)

        lbl3 = Label(frame2, text='La fecha actual es: ', bg='#9c2d2d')
        lbl3.place(x=3, y=105)
        lbl4 = Label(frame2, text=now.date(), bg='white')
        lbl4.place(x=3, y=125)

        self.btGuardar = Button(frame2, text='Guardar', command=self.fGuardar, bg='green', fg='black')
        self.btGuardar.place(x=10, y=170, width=60, height=30)

        self.btCancelar = Button(frame2, text='Cancelar', command=self.fCancelar, bg='red', fg='black')
        self.btCancelar.place(x=80, y=170, width=60, height=30)

        #creacion de la tabla
        frame3 = Frame(self, bg='#9c2d2d')
        frame3.place(x=252,y=0,width=460,height=260)
        self.grid = ttk.Treeview(frame3, columns=('#1','#2','#3','#4'))
        self.grid.column('#0',width=50)
        self.grid.column('#1', width=90, anchor=CENTER)
        self.grid.column('#2', width=150, anchor=W)
        self.grid.column('#3', width=75, anchor=CENTER)
        self.grid.column('#4', width=75, anchor=CENTER)


        self.grid.heading('#0', text='TASKID', anchor=CENTER)
        self.grid.heading('#1', text='TASKNAME', anchor=CENTER)
        self.grid.heading('#2', text='TASKDESCRIPTION', anchor=CENTER)
        self.grid.heading('#3', text='TASKACTIVE', anchor=CENTER)
        self.grid.heading('#4', text='TASKDATE', anchor=CENTER)
        self.grid.pack(side=LEFT,fill = Y)

        sb = Scrollbar(frame3, orient=VERTICAL)
        sb.pack(side=RIGHT,  fill = Y)
        self.grid.config(yscrollcommand=sb.set)
        sb.config(command=self.grid.yview())