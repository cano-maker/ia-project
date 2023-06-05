
if __name__ == '__main__':
	print("\n\nLa ejecución del programa no debería realizarse desde este archivo.")
	exit()

import tkinter as tk
from tkinter.messagebox import askyesno



class Ventana_App:
	def __init__(self, Obj_Tasks):
		self.MostrarDialogo = lambda titulo='test', mensaje='mensaje de prueba' : askyesno(title=titulo, message=mensaje)
		self.ObjTasks = Obj_Tasks
		self.window = tk.Tk()
		self.window.title("Space Titanic")
		self.window.geometry("800x800")
		self.window.resizable(width=False,height=False)

		self.label = tk.Label(self.window, justify='left', text="Segunda entrega inteligencia artificial!\n\n", background="white", anchor='nw')
		self.label.place(x=10,y=10,width=600,height=780)
	
		Btn_CrearBD = tk.Button(self.window, text="Crear BD", command=self.Btn_CrearBD_Click)
		Btn_CrearBD.place(x=630,y=105,width=100,height=30)

		Btn_PoblarBD = tk.Button(self.window, text="Poblar BD", command=self.Btn_PoblarBD_Click)
		Btn_PoblarBD.place(x=630,y=135,width=100,height=30)

		Btn_QueryPruebas = tk.Button(self.window, text="Query de prueba", command=self.Btn_QueryPruebas_Click)
		Btn_QueryPruebas.place(x=630,y=165,width=100,height=30)
		
		Btn_Ptrainer = tk.Button(self.window, text="Passenger Trainer", command=self.Btn_Ptrainer_Click)
		Btn_Ptrainer.place(x=630,y=225,width=100,height=30)
		
		Reset_Boton = tk.Button(self.window, text="Reset", command=self.BorrarTexto)
		Reset_Boton.place(x=630,y=195,width=100,height=30)


	def BorrarTexto(self):
		self.label.configure(text='')
		
	def AgregarLinea(self, Linea = 'Hola mundo'):
		TextoLabel = self.label.cget("text")
		self.label.configure(text=f'{TextoLabel}\n{Linea}')
		
	def Btn_CrearBD_Click(self):
		self.ObjTasks.Obj_Init_BD.CrearBD()
		self.ObjTasks.Obj_Init_BD.Crear_Tablas()
		#self.Actualizar_Label("se clickeo crear BD")
	
	def Btn_PoblarBD_Click(self):
		self.ObjTasks.Poblar_BD.Llenar_Tablas_Desde_CSV()
		
	def Btn_QueryPruebas_Click(self):
		self.AgregarLinea('\nEjecutando query de prueba:')
		QueryPruebas = 'SELECT * FROM passenger ORDER BY RANDOM() LIMIT 10;'
		self.AgregarLinea(QueryPruebas)
		self.ObjTasks.Obj_Init_BD.query_database(QueryPruebas)
		self.AgregarLinea('\nTarea completada.\n')
		pass
	
	def Btn_Ptrainer_Click(self):
		self.AgregarLinea('Comienzo de la analítica')
		self.ObjTasks.PTrainer.run()
		self.AgregarLinea('\nTarea completada con exito!\n')
		pass
	# self.Actualizar_Label("se clickeo crear BD")
	
	def button_b_clicked(self, titulo='cerrar el programa', mensaje='cerrar la app?'):
		answer = self.MostrarDialogo(titulo, mensaje)
		if answer:
			exit()
		self.Actualizar_Label("You clicked B\nHere is another line.")

	def button_c_clicked(self):
		self.Actualizar_Label("You clicked C\nAnd here is a third line.")
	
	def Actualizar_Label(self, message):
		self.label.configure(text=message)
	
	def ImportarMetodos(self, CrearBD):
		self.CrearBD = CrearBD

	def run(self):
		self.window.mainloop()

# Create an instance of the ButtonWindow class and run the application
#button_window = Ventana_App()
#button_window.run()