from tkinter import ttk
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

import matplotlib.pyplot as plt

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

		for F in (MainView, ArithmeticView):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row = 0, column = 0, sticky="nsew")

		self.show_frame(MainView)
   
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()


class MainView(tk.Frame):
    
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
		button_2 = ttk.Button(btn_container, text="Geométricas") 
		button_1.grid(row=1, column=0, padx=20, pady=50)
		button_2.grid(row=1, column=1, padx=20, pady=50)

		

class ArithmeticView(tk.Frame):
	
	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller

		self.file_a = None
		self.file_b = None
		self.img_a = {} ## Utilizo esto porque python borra la referencia de la imagen al salir de la funcion
		self.img_b = {}
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
		# sqrt_btn = ttk.Button(btn_list_container, text="").pack(pady=10, padx=10, fill="x", expand=True)
		# cbrt = ttk.Button(btn_list_container).pack(pady=10, padx=10, fill="x", expand=True)


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

		self.file_a = tk.Canvas(main_container, width=300, height=300, bg="red")
		self.file_a.id = "A"
		self.file_a.bind("<Button-1>", self.load_image)
		self.file_a.grid(row=2, column=0, pady=80)

		self.file_b = tk.Canvas(main_container, width=300, height=300, bg="red")
		self.file_b.id = "B"
		self.file_b.grid(row=2, column=1, pady=100)
		self.file_b.bind("<Button-1>", self.load_image)


	def load_image(self, event):
		
		path = filedialog.askopenfilename()


		if not path:
			raise FileNotFoundError

		canvas_clicked = event.widget
		
		pil_img = Image.open(path).resize((300,300)).convert("RGB")

		img = ImageTk.PhotoImage(image=pil_img)


		self.img_b[canvas_clicked.id] = pil_img ## Guardo tano pil como imagetk

		self.img_a[canvas_clicked.id] = img

		# canvas_clicked.delete('all')
		canvas_clicked.create_image(0,0, anchor='nw', image=img)

		print(self.img_a)
			

	def add_images(self):
		## First convert PIL to numpy array	

		## Verificar shapes de la imagen y ver si tienne los canales completos o x

		## Convert to 3 channels



		A, B = np.array(self.img_b['A'],dtype=np.float32), np.array(self.img_b['B'],dtype=np.float32)
		
		M,N,O = A.shape

		result = np.zeros((M,N,O))

		alpha = 0.5

		result = alpha * A + (1-alpha)*B

		self.show_result(np.clip(result, 0, 255).astype(np.uint8))



	def subrtact_images(self):


		A, B = np.array(self.img_b['A'],dtype=np.float32), np.array(self.img_b['B'],dtype=np.float32)
		
		M,N,O = A.shape

		result = np.zeros((M,N,O))

		result = A - B

		self.show_result(np.clip(result, 0, 255).astype(np.uint8))



	def multiply(self):

		A, B = np.array(self.img_b['A'],dtype=np.float32), np.array(self.img_b['B'],dtype=np.float32)
		
		M,N,O = A.shape

		result = np.zeros((M,N,O))

		alpha = 0.5

		result = A * B

		self.show_result(np.clip(result, 0, 255).astype(np.uint8))



	def show_result(self, image):
		plt.imshow(image)
		plt.show()

	pass


myapp = App()
myapp.mainloop()