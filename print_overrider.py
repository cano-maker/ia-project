import sys

class print_overrider:
	def __init__(self, LabelWritter):
		self.LabelWritter = LabelWritter
		#self.stdout = sys.stdout  # Store the original stdout object

	def JVelez_print(self, *args, **kwargs):
		# Custom print functionality
		# You can implement your own logic here
		#self.stdout.write("Custom print function: ")
		self.LabelWritter(" ".join(map(str, args)))
		#self.stdout.write("\n")
		#self.stdout.flush()


# Call the overridden print function
#print("Hello", "world!")
