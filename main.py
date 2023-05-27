import Inicializar_BD, Poblar_BD
from passenger_predictor import PassengerPredictor
from passenger_trainer import PassengerTrainer


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
	#main()
	user = 'postgres'
	password = 'postgres'
	host = 'localhost'
	port = '5432'
	database_name = 'spaceship_titanic'

	db_url = f'postgresql://{user}:{password}@{host}:{port}/{database_name}'

	passengerTrainer = PassengerTrainer(db_url)
	passengerTrainer.run()





