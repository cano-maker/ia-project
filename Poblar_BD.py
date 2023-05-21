import pandas as pd
import psycopg2
from psycopg2 import IntegrityError
from psycopg2.errors import DatatypeMismatch, NumericValueOutOfRange, UndefinedTable
import DB_Structure

class Poblar_BD:
	def __init__(self):
		DB_Params = DB_Structure.DB_Structure()
		self.csv = DB_Params.csv()
		self.Usuario = DB_Params.Usuario()
		self.Password = DB_Params.Password()
		self.Servidor = DB_Params.Servidor()
		self.Puerto = DB_Params.Puerto()
		self.Nombre_BD = DB_Params.Nombre_BD()
		self.Estructura_tablas = DB_Params.Estructura_tablas()

	def Llenar_Tablas_Desde_CSV(self):
		print('Iniciando el llenado de tablas ...')
		# Leer CSV en DataFrame de Pandas
		df = pd.read_csv(self.csv)
		#Conectar con BD
		conn = psycopg2.connect(dbname=self.Nombre_BD, host=self.Servidor, user=self.Usuario, password=self.Password, port=self.Puerto)
		cursor = conn.cursor()
		# String de apoyo para troubleshooting
		AuxQuery = ''
		# Llenar las tablas con datos
		for Nombre_Tabla, Estructura_tabla in self.Estructura_tablas.items():
			table_columns = list(Estructura_tabla.keys())
			insert_query = self.__build_insert_query(Nombre_Tabla, table_columns)
			for _, row in df.iterrows():
				insert_values = []
				for column in table_columns:
					value = row[column]
					if isinstance(value, float) and pd.isna(value):
						if Estructura_tabla[column]["type"] == "boolean": # Handle nan values
							value = False # Algunas filas no tienen boleanos inicializados
						elif Estructura_tabla[column]["type"] == "int":
							value = 30 # Algunas filas no tienen edad inicializada
					insert_values.append(value)
				try:
					AuxQuery = insert_query % tuple(insert_values)
					#print(AuxQuery)
					cursor.execute(insert_query, insert_values)
				except IntegrityError:
					# Manejo de excepciones para primary key duplicadas
					print(f"Saltando fila duplicada: {insert_values}")
				except DatatypeMismatch as e:
					print(f'Excepcion encontrada:\n{e}.\n\nFila problemática:\n{AuxQuery}')
					input()
				except NumericValueOutOfRange as e:
					print(f'Excepcion encontrada:\n{e}.\n\nFila problemática:\n{AuxQuery}')
					input()
				except UndefinedTable as e:
					print(f'Excepcion encontrada:\n{e}.\n\nFila problemática:\n{AuxQuery}')
					input()
		conn.commit()
		cursor.close()
		conn.close()
		print('llenado de tablas completado!\n')

	def __build_insert_query(self, table_name, table_columns):
		# Build the INSERT INTO query
		insert_query = f"INSERT INTO {table_name} ({', '.join(table_columns)}) VALUES "
		value_placeholders = ', '.join(['%s'] * len(table_columns))
		insert_query += f"({value_placeholders});"
		return insert_query

#ObjTemp = Poblar_BD()
#ObjTemp.Llenar_Tablas_Desde_CSV()
#fill_tables_from_csv()

