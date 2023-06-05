
if __name__ == '__main__':
	print("\n\nLa ejecución del programa no debería realizarse desde este archivo.")
	exit()

import pandas as pd
import psycopg2
from psycopg2 import IntegrityError
from psycopg2.errors import DatatypeMismatch, NumericValueOutOfRange, UndefinedTable, InFailedSqlTransaction
from DB_Structure import DB_Structure

class Poblar_BD:
	def __init__(self, CustomPrint=print):
		self.CustomPrint = CustomPrint
		DB_Params = DB_Structure()
		self.__CSV_File = DB_Params.csv()
		self.__Usuario = DB_Params.Usuario()
		self.__Password = DB_Params.Password()
		self.__Servidor = DB_Params.Servidor()
		self.__Puerto = DB_Params.Puerto()
		self.__Nombre_BD = DB_Params.Nombre_BD()
		self.__Estructura_tablas = DB_Params.Estructura_tablas()

	def Llenar_Tablas_Desde_CSV(self):
		#print('entró al método')
		print = self.CustomPrint # Sobreescribir el comportamiento de print
		print('Iniciando el llenado de tablas ...')
		# Leer CSV en DataFrame de Pandas
		df = pd.read_csv(self.__CSV_File)
		#Conectar con BD
		conn = psycopg2.connect(dbname=self.__Nombre_BD, host=self.__Servidor, user=self.__Usuario, password=self.__Password, port=self.__Puerto)
		cursor = conn.cursor()
		# String de apoyo para troubleshooting
		AuxQuery = ''
		# Llenar las tablas con datos
		for Nombre_Tabla, Estructura_tabla in self.__Estructura_tablas.items():
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
					#input()
				except NumericValueOutOfRange as e:
					print(f'Excepcion encontrada:\n{e}.\n\nFila problemática:\n{AuxQuery}')
					#input()
				except UndefinedTable as e:
					print(f'Excepcion encontrada:\n{e}.\n\nFila problemática:\n{AuxQuery}')
					#input()
				except Exception as e:
					print(f"Exepción por gestionar: {e}\nFila problemática:\n{AuxQuery}")
					#input()
					
		conn.commit()
		cursor.close()
		conn.close()
		print('llenado de tablas completado!\n')

	def __build_insert_query(self, table_name, table_columns):
		# Build the INSERT INTO query
		insert_query = f"INSERT INTO {table_name} ({', '.join(table_columns)}) VALUES "
		value_placeholders = ', '.join(['%s'] * len(table_columns))
		insert_query += f"({value_placeholders})"
		insert_query += ' on conflict do nothing;'
		#insert_query += ';' # debug
		return insert_query
	
	def query_database(self, query): # Debug
		print = self.CustomPrint # Sobreescribir el comportamiento de print
		conn = psycopg2.connect(host=self.__Servidor, port= self.__Puerto, dbname=self.__Nombre_BD, user=self.__Usuario, password=self.__Password)
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


#ObjTemp = Poblar_BD()
#ObjTemp.Llenar_Tablas_Desde_CSV()
#fill_tables_from_csv()

