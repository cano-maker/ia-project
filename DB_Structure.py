class DB_Structure:
	def __init__(self):
		self.__csv = './resources/test.csv'
		self.__Usuario = 'postgres'
		self.__Password = 'postgres'
		self.__Servidor = '127.0.0.1'
		self.__Puerto = '5432'
		self.__Nombre_BD = 'spaceship_titanic'  # postgres siempre crea bd en minusculas!!! si pones mayuscula, rompe el código
		self.__Estructura_tablas = {
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

	def csv(self):
		return self.__csv

	def Usuario(self):
		return self.__Usuario

	def Password(self):
		return self.__Password

	def Servidor(self):
		return self.__Servidor

	def Puerto(self):
		return self.__Puerto

	def Nombre_BD(self):
		return self.__Nombre_BD

	def Estructura_tablas(self):
		return self.__Estructura_tablas

