from tkinter import ttk
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

import matplotlib.pyplot as plt

from image_ops import ImageOps
from geometric_ops import GeometricOps

operations = ImageOps()

geometricops = GeometricOps()

class BaseOps(tk.Frame):

	def __init__(self, master):
		super().__init__(master)

		self.images = {}
		self.canva_info = None
		self.images_tk = {}

	def load_image(self, event):
		## Abrir explorador de archivos

		path = filedialog.askopenfilename()

		if not path:
			raise FileNotFoundError ## Cambiar por mensaje de error

		self.canva_info = event.widget

		pil_img = Image.open(path).resize((300,300)).convert("RGB")

		img = ImageTk.PhotoImage(image=pil_img)

		self.images[self.canva_info.id] = pil_img
		self.images_tk[self.canva_info.id] = img

		self.canva_info.delete('all')
		self.canva_info.create_image(0,0, anchor='nw', image=img)

		pass
	
	def show_result(self, image):
		plt.imshow(image)
		plt.show()


class App(tk.Tk):

	def __init__(self):
		super().__init__()
		self.geometry("1000x600")
		self.configure(bg="#222831")

		container = tk.Frame(self)
		container.pack(fill="both", expand=True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {} ## Empty array of frames

		for F in (MainView, ArithmeticView, ArithmeticScalar, GeometricView):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row = 0, column = 0, sticky="nsew")

		self.show_frame(MainView)
   
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

################## Ventanas o vistas #### Separar
class MainView(BaseOps):
    
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller
		self.load_widgets()

	def load_widgets(self):
		
		lab = Label(self, text="IMAGELAB", font=("Arial", 28, "bold"),fg="white" ,bg="#222831")
		lab.pack(side="top", fill="both")

		con = tk.Frame(self, bg ="#222831")
		con.pack(fill='both')
		description_label = Label(con, text="Podrás realizar las siguientes transformaciones:", fg="white", bg="#222831")
		description_label.pack(pady=(40,0), fill="both")

		btn_container = tk.Frame(self, bg="#222831")
		btn_container.grid_columnconfigure(0, weight=1)
		btn_container.grid_columnconfigure(1, weight=1)
		btn_container.pack(fill="both", expand=True)

	
		
		style = ttk.Style()
		style.configure('TButton', font = 
			('Arial', 14, 'bold'))

		button_1 = ttk.Button(btn_container, text="Aritméticas", style="TButton", command=lambda: self.controller.show_frame(ArithmeticView) ) 
		button_3 = ttk.Button(btn_container, text="Aritméticas con escalar", command=lambda: self.controller.show_frame(ArithmeticScalar)) ##Nombre 
		button_2 = ttk.Button(btn_container, text="Geométricas", command=lambda : self.controller.show_frame(GeometricView))
		button_1.grid(row=1, column=0, padx=20, pady=50)
		button_2.grid(row=1, column=1, padx=20, pady=50)
		button_3.grid(row=1, column=2, padx=20, pady=50)

		

class ArithmeticView(BaseOps):
	
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller

		self.file_a = None
		self.file_b = None
		self.img_container = {} ## Utilizo esto porque python borra la referencia de la imagen al salir de la funcion
		self.load_widgets()

	def load_widgets(self):
		
		lab = Label(self, text="IMAGELAB", font=("Arial", 28, "bold"),fg="white" ,bg="#222831")
		lab.pack(side="top", fill="both")


		## Sidebar que contendrá los botones en lista de las operaciones a realizar
		con = tk.Frame(self, bg ="#222831")
		con.pack(fill='y', side="right")
		
		lab = Label(con, text="Operaciones", font=("Arial", 28, "bold"),fg="white" ,bg="#222831")
		lab.pack(side="top", fill="both")


		btn_list_container = tk.Frame(con, bg ="#222831")
		btn_list_container.grid_columnconfigure(0, weight=1)
		btn_list_container.pack(fill='y', side="right")


		inner = tk.Frame(btn_list_container, bg="#222831")
		inner.pack(expand=True, fill="y")



		add_btn = ttk.Button(inner, text="Suma", style="TButton", command=self.add_images).pack(pady=10, fill="x", expand=True)
		subtract_btn = ttk.Button(inner, text="Resta", command=self.subrtact_images).pack(pady=10, fill="x", expand=True)
		multiply_image = ttk.Button(inner, text="Multiplicar", command=self.multiply).pack(pady=10, fill="x", expand=True)


		####################### Esta sección contiene los recuadros que contendrán las imagenes.

		# Main container tiene las imágenes con las que se realizaran los calculos
		main_container = tk.Frame(self, bg="#222831")
		main_container.pack(fill="both", expand=True)
		main_container.grid_columnconfigure(0, weight=1)
		main_container.grid_columnconfigure(1, weight=1)


		# Label

		description = Label(main_container, text="Sube las imagenes con las que quieres realizar las operaciones", font=("Arial", 10, "bold"),fg="white" ,bg="#222831")
		description.grid(row=1, column=1)

		## Recuadros

		self.file_a = tk.Canvas(main_container, width=300, height=300, bg="red")
		self.file_a.id = "A"
		self.file_a.bind("<Button-1>", self.load_image)
		self.file_a.grid(row=2, column=0, pady=80)

		self.file_b = tk.Canvas(main_container, width=300, height=300, bg="red")
		self.file_b.id = "B"
		self.file_b.grid(row=2, column=1, pady=100)
		self.file_b.bind("<Button-1>", self.load_image)

	
	def add_images(self):
		self.show_result(operations.add_images(self.images["A"], self.images["B"], 0.5))


	def subrtact_images(self):

		self.show_result(operations.subtract_images(self.images["A"], self.images["B"]))



	def multiply(self):

		self.show_result(operations.multiply_images(self.images["A"], self.images["B"]))
	
	pass


class ArithmeticScalar(BaseOps):
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller
		self.entry = None
		self.value = 0.5 ## Guarda el escalar. por defecto 0.5
		# self.file = None
		# self.image = {}
		# self.image_tk = {}
		# self.scalar = None
		self.load_widgets()


	def load_widgets(self):

		lab = Label(self, text="IMAGELAB", font=("Arial", 28, "bold"),fg="white" ,bg="#222831")
		lab.pack(side="top", fill="both")


		## Sidebar que contendrá los botones en lista de las operaciones a realizar
		con = tk.Frame(self, bg ="#222831")
		con.pack(fill='y', side="right")
		
		lab = Label(con, text="Operaciones", font=("Arial", 28, "bold"),fg="white" ,bg="#222831")
		lab.pack(side="top", fill="both")


		btn_list_container = tk.Frame(con, bg ="#222831")
		btn_list_container.grid_columnconfigure(0, weight=1)
		btn_list_container.pack(fill='y', side="right")


		inner = tk.Frame(btn_list_container, bg="#222831")
		inner.pack(expand=True, fill="y")



		square_btn = ttk.Button(inner, text="Funcion cuadrada", style="TButton", command=self.square_scalar).pack(pady=10, fill="x", expand=True)
		cubic_btn = ttk.Button(inner, text="Cubica", command=self.cubic_scalar).pack(pady=10, fill="x", expand=True)
		add_scalar = ttk.Button(inner, text="Sumar a un escalar", command=self.add_scalar).pack(pady=10, fill="x", expand=True)
		subtract_scalar =  ttk.Button(inner, text="Restar a un escalar", command=self.subtract_scalar).pack(pady=10, fill="x", expand=True)
		divide_scalar =  ttk.Button(inner, text="Dividir por un escalar", command=self.divide_scalar).pack(pady=10, fill="x", expand=True)
		multiply_scalar =  ttk.Button(inner, text="Multiplicar por un escalar", command=self.multiply_scalar).pack(pady=10, fill="x", expand=True)

		####################### Esta sección contiene lsos recuadros que contendrán las imagenes.

		# Main container tiene las imágenes con las que se realizaran los calculos
		main_container = tk.Frame(self, bg="#222831")
		main_container.pack(fill="both", expand=True)
		main_container.grid_columnconfigure(0, weight=1)
		main_container.grid_columnconfigure(1, weight=1)


		# Label

		description = Label(main_container, text="Sube las imagenes con las que quieres realizar las operaciones", font=("Arial", 10, "bold"),fg="white" ,bg="#222831")
		description.grid(row=1, column=1)

		## Recuadros

		self.file = tk.Canvas(main_container, width=300, height=300, bg="red")
		self.file.id = "A"
		self.file.bind("<Button-1>", self.load_image)
		self.file.grid(row=2, column=0, pady=80)


		## Frame para escalar

		scalar_frame = tk.Frame(self, bg="#222831")
		scalar_frame.pack(fill="y")
		scalar_frame.grid_columnconfigure(0, weight=1)

		self.entry = tk.Entry(scalar_frame)
		self.entry.pack( fill="y", side="left")

		set_scalar_btn = tk.Button(scalar_frame, text="Set scalar", command=self.set_scalar)
		set_scalar_btn.pack(fill="y", side="right")
		


	def set_scalar(self):
		self.value = float(self.entry.get())

	def square_scalar(self):

		self.show_result(operations.square_scalar(self.images["A"]))
		
		pass

	def cubic_scalar(self):

		self.show_result(operations.cubic_scalar(self.images["A"]))

		pass
        
	def add_scalar(self):

		self.show_result(operations.add_scalar(self.images["A"], self.value))
		pass


	def subtract_scalar(self):

		self.show_result(operations.subtract_scalar(self.images["A"], self.value))

		pass


	def multiply_scalar(self):

		self.show_result(operations.multiply_scalar(self.images["A"], self.value))

		pass


	def divide_scalar(self):
		self.show_result(operations.divide_scalar(self.images["A"], self.value))
		pass


class GeometricView(BaseOps):
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller
		self.entry = None
		self.value = 0.5 ## Guarda el escalar. por defecto 0.5
		# self.file = None
		# self.image = {}
		# self.image_tk = {}
		# self.scalar = None
		self.load_widgets()


	def load_widgets(self):

		lab = Label(self, text="IMAGELAB", font=("Arial", 28, "bold"),fg="white" ,bg="#222831")
		lab.pack(side="top", fill="both")


		## Sidebar que contendrá los botones en lista de las operaciones a realizar
		con = tk.Frame(self, bg ="#222831")
		con.pack(fill='y', side="right")
		
		lab = Label(con, text="Operaciones", font=("Arial", 28, "bold"),fg="white" ,bg="#222831")
		lab.pack(side="top", fill="both")


		btn_list_container = tk.Frame(con, bg ="#222831")
		btn_list_container.grid_columnconfigure(0, weight=1)
		btn_list_container.pack(fill='y', side="right")


		inner = tk.Frame(btn_list_container, bg="#222831")
		inner.pack(expand=True, fill="y")



		rotate_btn = ttk.Button(inner, text="Rotar", style="TButton", command=self.rotate).pack(pady=10, fill="x", expand=True)
		translate_btn = ttk.Button(inner, text="Trasladar", command=self.translate).pack(pady=10, fill="x", expand=True)
		
		####################### Esta sección contiene lsos recuadros que contendrán las imagenes.

		# Main container tiene las imágenes con las que se realizaran los calculos
		main_container = tk.Frame(self, bg="#222831")
		main_container.pack(fill="both", expand=True)
		main_container.grid_columnconfigure(0, weight=1)
		main_container.grid_columnconfigure(1, weight=1)


		# Label

		description = Label(main_container, text="Sube las imagenes con las que quieres realizar las operaciones", font=("Arial", 10, "bold"),fg="white" ,bg="#222831")
		description.grid(row=1, column=1)

		## Recuadros

		self.file = tk.Canvas(main_container, width=300, height=300, bg="red")
		self.file.id = "A"
		self.file.bind("<Button-1>", self.load_image)
		self.file.grid(row=2, column=0, pady=80)


	def rotate(self):
		pass

	def translate(self):

		bx = 50
		by = 40

		self.show_result(geometricops.traslation(bx,by, self.images["A"]))

		pass



class GeometricTransformations(BaseOps):
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller
		self.entry = None
		self.value = 0.5 ## Guarda el escalar. por defecto 0.5
		self.load_widgets()


	def load_widgets(self):

		lab = Label(self, text="IMAGELAB", font=("Arial", 28, "bold"),fg="white" ,bg="#222831")
		lab.pack(side="top", fill="both")


		## Sidebar que contendrá los botones en lista de las operaciones a realizar
		con = tk.Frame(self, bg ="#222831")
		con.pack(fill='y', side="right")
		
		lab = Label(con, text="Operaciones", font=("Arial", 28, "bold"),fg="white" ,bg="#222831")
		lab.pack(side="top", fill="both")


		btn_list_container = tk.Frame(con, bg ="#222831")
		btn_list_container.grid_columnconfigure(0, weight=1)
		btn_list_container.pack(fill='y', side="right")


		inner = tk.Frame(btn_list_container, bg="#222831")
		inner.pack(expand=True, fill="y")



		square_btn = ttk.Button(inner, text="Funcion cuadrada", style="TButton", command=self.square_scalar).pack(pady=10, fill="x", expand=True)
		cubic_btn = ttk.Button(inner, text="Cubica", command=self.cubic_scalar).pack(pady=10, fill="x", expand=True)
		add_scalar = ttk.Button(inner, text="Sumar a un escalar", command=self.add_scalar).pack(pady=10, fill="x", expand=True)
		subtract_scalar =  ttk.Button(inner, text="Restar a un escalar", command=self.subtract_scalar).pack(pady=10, fill="x", expand=True)
		divide_scalar =  ttk.Button(inner, text="Dividir por un escalar", command=self.divide_scalar).pack(pady=10, fill="x", expand=True)
		multiply_scalar =  ttk.Button(inner, text="Multiplicar por un escalar", command=self.multiply_scalar).pack(pady=10, fill="x", expand=True)

		####################### Esta sección contiene lsos recuadros que contendrán las imagenes.

		# Main container tiene las imágenes con las que se realizaran los calculos
		main_container = tk.Frame(self, bg="#222831")
		main_container.pack(fill="both", expand=True)
		main_container.grid_columnconfigure(0, weight=1)
		main_container.grid_columnconfigure(1, weight=1)


		# Label

		description = Label(main_container, text="Sube las imagenes con las que quieres realizar las operaciones", font=("Arial", 10, "bold"),fg="white" ,bg="#222831")
		description.grid(row=1, column=1)

		## Recuadros

		self.file = tk.Canvas(main_container, width=300, height=300, bg="red")
		self.file.id = "A"
		self.file.bind("<Button-1>", self.load_image)
		self.file.grid(row=2, column=0, pady=80)


		## Frame para escalar

		scalar_frame = tk.Frame(self, bg="#222831")
		scalar_frame.pack(fill="y")
		scalar_frame.grid_columnconfigure(0, weight=1)

		self.entry = tk.Entry(scalar_frame)
		self.entry.pack( fill="y", side="left")

		set_scalar_btn = tk.Button(scalar_frame, text="Set scalar", command=self.set_scalar)
		set_scalar_btn.pack(fill="y", side="right")
		


	def set_scalar(self):
		self.value = float(self.entry.get())

	def square_scalar(self):

		self.show_result(operations.square_scalar(self.images["A"]))
		
		pass

	def cubic_scalar(self):

		self.show_result(operations.cubic_scalar(self.images["A"]))

		pass
        
	def add_scalar(self):

		self.show_result(operations.add_scalar(self.images["A"], self.value))
		pass


	def subtract_scalar(self):

		self.show_result(operations.subtract_scalar(self.images["A"], self.value))

		pass


	def multiply_scalar(self):

		self.show_result(operations.multiply_scalar(self.images["A"], self.value))

		pass


	def divide_scalar(self):
		self.show_result(operations.divide_scalar(self.images["A"], self.value))
		pass




myapp = App()
myapp.mainloop()