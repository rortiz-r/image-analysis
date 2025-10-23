from tkinter import ttk
from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox
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
		plt.xticks([]) 
		plt.yticks([]) 
		plt.show()

	def verify_image(self, mode):
		if mode == 2:
			if "A" not in self.images or "B" not in self.images:
				messagebox.showerror("Error","Images can not be empty")
				return False
			return True
		if mode == 1:
			if "A" not in self.images:
				messagebox.showerror("Error","Images can not be empty")
				return False
			return True



class App(tk.Tk):

	def __init__(self):
		super().__init__()
		self.geometry("1200x600")
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
	

		## Recuadros

		self.file_a = tk.Canvas(main_container, width=300, height=300, bg="white")
		self.file_a.id = "A"
		self.file_a.bind("<Button-1>", self.load_image)
		self.file_a.grid(row=2, column=0, pady=80)

		self.file_b = tk.Canvas(main_container, width=300, height=300, bg="white")
		self.file_b.id = "B"
		self.file_b.grid(row=2, column=1, pady=100)
		self.file_b.bind("<Button-1>", self.load_image)

	
	def add_images(self):
		if self.verify_image(2):
			self.show_result(operations.add_images(self.images["A"], self.images["B"], 0.5))
		


	def subrtact_images(self):
		if self.verify_image(2):
			self.show_result(operations.subtract_images(self.images["A"], self.images["B"]))



	def multiply(self):
		if self.verify_image(2):
			self.show_result(operations.multiply_images(self.images["A"], self.images["B"]))
	

class ArithmeticScalar(BaseOps):
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller
		self.entry = None
		self.value = 5 ## Guarda el escalar. por defecto 0.5
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

	
		## Recuadros

		self.file = tk.Canvas(main_container, width=300, height=300, bg="white")
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
		if self.verify_image(1):
			self.show_result(operations.square_scalar(self.images["A"]))

	def cubic_scalar(self):

		if self.verify_image(1):
			self.show_result(operations.cubic_scalar(self.images["A"]))
		
		

		pass
        
	def add_scalar(self):
		if self.verify_image(1):
			self.show_result(operations.add_scalar(self.images["A"], self.value))


	def subtract_scalar(self):

		if self.verify_image(1):
			self.show_result(operations.subtract_scalar(self.images["A"], self.value))

		pass


	def multiply_scalar(self):
		
		if self.verify_image(1):
			self.show_result(operations.multiply_scalar(self.images["A"], self.value))


	def divide_scalar(self):
		if self.verify_image(1):
			self.show_result(operations.divide_scalar(self.images["A"], self.value))


class GeometricView(BaseOps):
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller
		self.entry = None
		self.value = 0.5 ## Guarda el escalar. por defecto 0.5

		## Definimos los atributos que contendrán los widgets entry

		self.bx = None
		self.by = None
		self.theta = None

		## Definimos los atributos que contendrán los valores ingresados

		self.bx_value = 0
		self.by_value = 0
		self.theta_value = 0

		## Cargamos los widgets.

		self.load_widgets()


	def load_widgets(self):

		lab = Label(self, text="IMAGELAB", font=("Arial", 28, "bold"), fg="white", bg="#222831")
		lab.pack(side="top", fill="x")

		con = tk.Frame(self, bg="#222831")
		con.pack(side="right", fill="y", padx=(0, 10), pady=10)

		lab = Label(con, text="Operaciones", font=("Arial", 20, "bold"), fg="white", bg="#222831")
		lab.pack(anchor="n", pady=10)

		btn_list_container = tk.Frame(con, bg="#393E46")
		btn_list_container.pack(fill="y", padx=10, pady=10)

		inner = tk.Frame(btn_list_container, bg="#393E46")
		inner.pack(expand=True, fill="y", padx=10, pady=10)

		traslate_frame = tk.LabelFrame(inner, text="Traslación", fg="white", bg="#393E46", font=("Arial", 12, "bold"), labelanchor="n")
		traslate_frame.pack(fill="x", pady=10)

		translate_btn = ttk.Button(traslate_frame, text="Trasladar", command=self.traslation)
		translate_btn.pack(fill="x", padx=10, pady=(10, 5))

		entries_frame = tk.Frame(traslate_frame, bg="#393E46")
		entries_frame.pack(pady=5)

		bx_frame = tk.Frame(entries_frame, bg="#393E46")
		bx_frame.pack(side="left", padx=10)
		bx_label = tk.Label(bx_frame, text="bx", fg="#ffffff", bg="#393E46")
		bx_label.pack(anchor="w")
		self.bx = tk.Entry(bx_frame)
		self.bx.pack()

		by_frame = tk.Frame(entries_frame, bg="#393E46")
		by_frame.pack(side="left", padx=10)
		by_label = tk.Label(by_frame, text="by", fg="#ffffff", bg="#393E46")
		by_label.pack(anchor="w")
		self.by = tk.Entry(by_frame)
		self.by.pack()

		set_bxby_btn = tk.Button(traslate_frame, text="OK", command=self.set_traslate_values)
		set_bxby_btn.pack(pady=(5, 10))

		rotation_frame = tk.LabelFrame(inner, text="Rotación", fg="white", bg="#393E46", font=("Arial", 12, "bold"), labelanchor="n")
		rotation_frame.pack(fill="x", pady=10)

		rotate_btn = ttk.Button(rotation_frame, text="Rotar", command=self.rotation)
		rotate_btn.pack(fill="x", padx=10, pady=(10, 5))

		entry_frame = tk.Frame(rotation_frame, bg="#393E46")
		entry_frame.pack(pady=5)

		theta_frame = tk.Frame(entry_frame, bg="#393E46")
		theta_frame.pack()
		theta_label = tk.Label(theta_frame, text="Theta", fg="#ffffff", bg="#393E46")
		theta_label.pack(anchor="w")
		self.theta = tk.Entry(theta_frame)
		self.theta.pack()

		set_theta_btn = tk.Button(rotation_frame, text="OK", command=self.set_theta_values)
		set_theta_btn.pack(pady=(5, 10))

		main_container = tk.Frame(self, bg="#222831")
		main_container.pack(fill="both", expand=True)
		main_container.grid_columnconfigure(0, weight=1)
		main_container.grid_columnconfigure(1, weight=1)

		self.file = tk.Canvas(main_container, width=300, height=300, bg="white")
		self.file.id = "A"
		self.file.bind("<Button-1>", self.load_image)
		self.file.grid(row=2, column=0, pady=80)


	def set_traslate_values(self):
		
		if self.bx.get() or self.by.get():
			self.bx_value = int(self.bx.get())
			self.by_value = int(self.by.get())
		else:
			messagebox.showerror("Error", "bx or by is empty")


	def set_theta_values(self):

		if self.theta.get():
			self.theta_value = int(self.theta.get())
		else:
			messagebox.showerror("Error", "Theta entry is empty")


	
	def rotation(self):

		if self.verify_image(1):
			result = geometricops.rotation(self.theta_value, self.images["A"])
			self.show_result(result)					
		pass
	
	def traslation(self):
		
		if self.verify_image(1):
			result = geometricops.traslation(self.bx_value, self.by_value, self.images["A"])
			self.show_result(result)

		pass

myapp = App()
myapp.mainloop()