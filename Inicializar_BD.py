import psycopg2, psycopg2.errors as SQLExcept2
import DB_Structure

class Inicializar_BD:
	def __init__(self):
		DB_Params = DB_Structure.DB_Structure()
		self.Usuario = DB_Params.Usuario()
		self.Password = DB_Params.Password()
		self.Servidor = DB_Params.Servidor()
		self.Puerto = DB_Params.Puerto()
		self.Nombre_BD = DB_Params.Nombre_BD()
		self.Estructura_tablas = DB_Params.Estructura_tablas()

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
		print('Tablas creadas con Exito!\n')

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

	"""
	################################
	####### Inicio Consulta ########
	################################
	"""
	def query_database(self, query):
		conn = psycopg2.connect(host=self.Servidor, port= self.Puerto, dbname=self.Nombre_BD, user=self.Usuario, password=self.Password)
		cursor = conn.cursor()
		try:
			cursor.execute(query)
			FilasConsulta = cursor.fetchall()
			for Fila in FilasConsulta:
				print(Fila)
		except Exception as e:
			print(f"Exepción por gestionar: {str(e)}")
			input()
		finally:
			cursor.close()
			conn.close()

	"""
	################################
	######## Fin Consulta ##########
	################################
	"""

#DB_Params = DB_Structure.DB_Structure()
#Obj_Init_BD = Inicializar_BD()
#Obj_Init_BD.CrearBD()
#Obj_Init_BD.Crear_Tablas()