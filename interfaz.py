import tkinter as tk
from tkinter import filedialog

def seleccionar_carpeta():
    ruta_carpeta = filedialog.askdirectory()
    label_ruta.config(text=ruta_carpeta)
    cuadro_texto.delete(0, tk.END)
    cuadro_texto.insert(0, ruta_carpeta)

def seleccionar_archivo():
    ruta_archivo = filedialog.askopenfilename()
    label_ruta.config(text=ruta_archivo)
    cuadro_texto.delete(0, tk.END)
    cuadro_texto.insert(0, ruta_archivo)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Seleccionar carpeta")
ventana.geometry("600x400")

# Crear un frame para contener los elementos
frame = tk.Frame(ventana)
frame.pack(fill="both")

# Crear una etiqueta para mostrar la ruta seleccionada dentro del frame
label_ruta = tk.Label(frame, text="Ruta seleccionada aparecerá aquí")
label_ruta.grid(row=0, column=0, columnspan=2, pady=10)

# Crear un botón para abrir el cuadro de diálogo de selección de carpetas dentro del frame
boton_seleccionar_carpeta = tk.Button(frame, text="Seleccionar carpeta", command=seleccionar_carpeta)
boton_seleccionar_carpeta.grid(row=1, column=0, pady=10)

# Crear un botón para abrir el cuadro de diálogo de selección de archivos dentro del frame
boton_seleccionar_archivo = tk.Button(frame, text="Seleccionar archivo", command=seleccionar_archivo)
boton_seleccionar_archivo.grid(row=1, column=1, pady=10)

# Crear un cuadro de texto para mostrar la ruta seleccionada dentro del frame
cuadro_texto = tk.Entry(frame, width=80)
cuadro_texto.grid(row=2, column=0, columnspan=2, pady=10)

# Iniciar el bucle principal de la interfaz
# ventana.mainloop()
