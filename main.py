import Inicializar_BD, Poblar_BD

class main:
	def __init__(self):
		self.Obj_Init_BD = Inicializar_BD.Inicializar_BD()
		self.Poblar_BD = Poblar_BD.Poblar_BD()
		self.Obj_Init_BD.CrearBD()
		self.Obj_Init_BD.Crear_Tablas()
		self.Poblar_BD.Llenar_Tablas_Desde_CSV()
		query = 'SELECT * FROM passenger ORDER BY RANDOM() LIMIT 10;'
		self.Obj_Init_BD.query_database(query)
		print('\nLarga vida al POO')
		pass

#Ejecutar = main()

if __name__ == '__main__':
	main()