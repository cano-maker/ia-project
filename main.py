from Inicializar_BD import Inicializar_BD
from Poblar_BD import Poblar_BD
from passenger_trainer import PassengerTrainer
from Ventana_App import Ventana_App
from print_overrider import print_overrider

class main:
	def __init__(self):
		self.Ventana = Ventana_App(self)
		ObjCprint = print_overrider(self.Ventana.AgregarLinea)

		self.Obj_Init_BD = Inicializar_BD(CustomPrint=ObjCprint.JVelez_print, dialogo = self.Ventana.MostrarDialogo)
		self.Poblar_BD = Poblar_BD(CustomPrint=ObjCprint.JVelez_print)
		self.PTrainer = PassengerTrainer(CustomPrint=ObjCprint.JVelez_print)
		
		self.Ventana.run()
		pass

if __name__ == '__main__':
	main()
else:
	print('Llamar el programa desde el archivo Main')




