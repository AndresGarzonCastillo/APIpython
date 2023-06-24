import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient

class Producto:
    db_name = 'ProductosPapeleria'

    def __init__(self, window):
        self.window = window
        self.window.title('Control Productos')

        frame = ttk.LabelFrame(self.window, text='Registrar Producto')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        ttk.Label(frame, text='Nombre Producto:').grid(row=1, column=0)
        self.nombre = ttk.Entry(frame)
        self.nombre.grid(row=1, column=1)

        ttk.Label(frame, text='Precio Producto').grid(row=2, column=0)
        self.precio = ttk.Entry(frame)
        self.precio.grid(row=2, column=1)

        ttk.Button(frame, text='Agregar Producto', command=self.agregar_datos).grid(row=3, columnspan=2, sticky='we')

        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Nombre', anchor=tk.CENTER)
        self.tree.heading('#1', text='Precio', anchor=tk.CENTER)
        self.get_productos()

    def get_database(self):
        client = MongoClient('mongodb://localhost:27017/')
        return client[self.db_name]

    def get_productos(self):
        db = self.get_database()
        collection = db['Productos']
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        for row in collection.find():
            self.tree.insert('', 'end', text=row['NombreProducto'], values=row['PrecioProducto'])

    def validacion(self):
        return len(self.nombre.get()) != 0 and len(self.precio.get()) != 0

    def agregar_datos(self):
        if self.validacion():
            db = self.get_database()
            collection = db['Productos']
            producto = {
                'NombreProducto': self.nombre.get(),
                'PrecioProducto': self.precio.get()
            }
            collection.insert_one(producto)
            self.get_productos()
            self.nombre.delete(0, tk.END)
            self.precio.delete(0, tk.END)


if __name__ == '__main__':
    window = tk.Tk()
    application = Producto(window)
    window.mainloop()
