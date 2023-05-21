import pandas as pd
import psycopg2, psycopg2.errors as SQLExcept2

##############################
##### Inicializar Valores ####
##############################

Usuario = 'postgres'
Password = 'postgres'
Servidor = '127.0.0.1'
Puerto = '5432'
Nombre_BD = 'spaceship_titanic' # postgres siempre crea bd en minusculas!!! si pones mayuscula, rompe el código
Estructura_tablas = {
	"passenger": {
		"PassengerId": {"type": "varchar(30)", "primary_key": True},
		"HomePlanet": {"type": "varchar(30)"},
		"CryoSleep": {"type": "boolean"},
		"Cabin": {"type": "varchar(30)"},
		"Destination": {"type": "varchar(30)"},
		"Age": {"type": "int"},
		"VIP": {"type": "boolean"},
		"Name": {"type": "varchar(50)"}
	},
	"Services": {
		"PassengerId": {"type": "varchar(30)", "primary_key": True, "foreign_key": "passenger(PassengerId)"},
		"RoomService": {"type": "int"},
		"FoodCourt": {"type": "int"},
		"ShoppingMall": {"type": "int"},
		"Spa": {"type": "int"},
		"VRDeck": {"type": "int"}
	}
}

""" 
### Codigo para pruebas unitarias

Estructura_tablas = { 
	"Customer": {
		"Customer_ID": {"type": "int", "primary_key": True},
		"Customer_Name": {"type": "varchar(30)"}
	},
	"Car_Pool": {
		"Reference_ID": {"type": "int", "primary_key": True},
		"Reference_Name": {"type": "varchar(20)"}
	},
	"Sold_Car": {
		"Reference_ID": {"type": "int", "foreign_key": "Car_Pool(Reference_ID)", "primary_key": True},
		"Customer_ID": {"type": "int", "foreign_key": "Customer(Customer_ID)", "primary_key": True},
		"Color": {"type": "varchar(15)"}
	}
}
"""

##################################
##### Fin Inicializar Valores ####
##################################


class Inicializar_BD:

	def __init__(self, Usuario, Password, Servidor, Puerto, Nombre_BD, Estructura_tablas):
		self.Usuario = Usuario
		self.Password = Password
		self.Servidor = Servidor
		self.Puerto = Puerto
		self.Nombre_BD = Nombre_BD
		self.Estructura_tablas = Estructura_tablas

	###################
	##### Crear BD ####
	###################
	def CrearBD(self, recrear = False):
		Count = conn = 0
		try:
			conn = psycopg2.connect(host=self.Servidor, user=self.Usuario, password=self.Password, port= self.Puerto)
			Count += 1
			conn.autocommit = True
			cursor = conn.cursor()
			if recrear:
				Query = 'drop database ' + self.Nombre_BD
				cursor.execute(Query)
				print('Base de datos borrada correctamente')
			Query = 'create database ' + self.Nombre_BD
			cursor.execute(Query)
			print("Base de datos creada!\n")
		except SQLExcept2.DuplicateDatabase as e:
			print('La base de datos"', self.Nombre_BD, '"ya existe.')
			print('Desea recrear la BD?', '1 - Si', 'Cualquier otro valor para omitir creación', sep = '\n')
			val = input()
			#val = '1' # Debug
			print()
			if val == '1':
				self.CrearBD(recrear = True)
			else:
				print('Omitiendo Creación de la BD')
		except SQLExcept2.OperationalError as e:
			if Count == 0:
				print('La conexión falló. revisa los parámetros y asegurate que hay un servidor a la escucha')
				print(e)
			else:
				print("La conexión se estableció, pero la creación arrojó exepción no manejada correctamente. Revisar")
				raise # Troubleshooting
		finally:
			conn.close() #Cerrar la conexión
			pass

	######################
	#### Fin Crear BD ####
	######################

	################################
	##### Inicio Crear Tablas ######
	################################
	def Crear_Tablas(self):
		print('Iniciando creación de tablas ....')
		conn = psycopg2.connect(host=self.Servidor, port= self.Puerto, dbname=self.Nombre_BD, user=self.Usuario, password=self.Password)
		cursor = conn.cursor()

		for table_name, columns in self.Estructura_tablas.items():
			create_table_query = self.__build_create_query(table_name, columns)
			#print(create_table_query) # Borrar tras debug
			cursor.execute(create_table_query) #Comentado Temporalmente, debug

			for column_name, attributes in columns.items():
				foreign_key = attributes.get('foreign_key')
				if foreign_key:
					alter_table_query = self.__build_alter_query_FK(table_name, column_name, foreign_key)
					#print(alter_table_query) # Borrar tras debug
					cursor.execute(alter_table_query) #Comentado Temporalmente, debug
		conn.commit()
		cursor.close()
		conn.close()
		print('Tablas creadas con Exito!')

	def __build_create_query(self, table_name, columns):
		column_definitions = []
		primary_key = []
		for column_name, attributes in columns.items():
			column_type = attributes['type']
			column_definition = f"{column_name} {column_type}"
			if attributes.get('primary_key'):
				primary_key.append(column_name)
			column_definitions.append(column_definition)
		return f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_definitions)}, PRIMARY KEY ({', '.join(primary_key)}));"

	def __build_alter_query_FK(self, table_name, column_name, foreign_key):
		return f"ALTER TABLE {table_name} ADD FOREIGN KEY ({column_name}) REFERENCES {foreign_key};"

	"""
	################################
	###### Fin Crear Tablas ########
	################################
	"""

Obj_Init_BD = Inicializar_BD(Usuario, Password, Servidor, Puerto, Nombre_BD, Estructura_tablas)
Obj_Init_BD.CrearBD()
Obj_Init_BD.Crear_Tablas()
