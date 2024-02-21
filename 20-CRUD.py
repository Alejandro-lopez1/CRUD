import sqlite3
import tkinter as tk
from tkinter import messagebox

# Conexión a la base de datos (o la crea si no existe)
conn = sqlite3.connect('ejemplo.db')

# Crear tabla si no existe
conn.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                edad INTEGER
                )''')

def crear_usuario():
    nombre = nombre_entry.get()
    edad = edad_entry.get()
    conn.execute('INSERT INTO usuarios (nombre, edad) VALUES (?, ?)', (nombre, edad))
    conn.commit()
    messagebox.showinfo("Éxito", "Usuario creado con éxito.")
    limpiar_campos()
    mostrar_usuarios()

def editar_usuario():
    id_usuario = id_entry.get()
    nombre = nombre_entry.get()
    edad = edad_entry.get()
    conn.execute('UPDATE usuarios SET nombre = ?, edad = ? WHERE id = ?', (nombre, edad, id_usuario))
    conn.commit()
    messagebox.showinfo("Éxito", "Usuario actualizado con éxito.")
    limpiar_campos()
    mostrar_usuarios()

def eliminar_usuario():
    id_usuario = id_entry.get()
    conn.execute('DELETE FROM usuarios WHERE id = ?', (id_usuario,))
    conn.commit()
    messagebox.showinfo("Éxito", "Usuario eliminado con éxito.")
    limpiar_campos()
    mostrar_usuarios()

def seleccionar_usuario(event):
    index = usuarios_listbox.curselection()[0]
    usuario_seleccionado = usuarios_listbox.get(index)
    id_usuario = usuario_seleccionado.split(':')[1].strip()
    id_entry.delete(0, tk.END)
    id_entry.insert(tk.END, id_usuario)

def mostrar_usuarios():
    usuarios_listbox.delete(0, tk.END)
    cursor = conn.execute('SELECT id, nombre, edad FROM usuarios')
    for row in cursor:
        usuarios_listbox.insert(tk.END, f"ID: {row[0]}, Nombre: {row[1]}, Edad: {row[2]}")

def limpiar_campos():
    id_entry.delete(0, tk.END)
    nombre_entry.delete(0, tk.END)
    edad_entry.delete(0, tk.END)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Aplicación CRUD de Usuarios")

# Crear widgets
id_label = tk.Label(root, text="ID:")
id_label.grid(row=0, column=0, padx=5, pady=5)

id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1, padx=5, pady=5)

nombre_label = tk.Label(root, text="Nombre:")
nombre_label.grid(row=1, column=0, padx=5, pady=5)

nombre_entry = tk.Entry(root)
nombre_entry.grid(row=1, column=1, padx=5, pady=5)

edad_label = tk.Label(root, text="Edad:")
edad_label.grid(row=2, column=0, padx=5, pady=5)

edad_entry = tk.Entry(root)
edad_entry.grid(row=2, column=1, padx=5, pady=5)

crear_button = tk.Button(root, text="Crear Usuario", command=crear_usuario)
crear_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="WE")

editar_button = tk.Button(root, text="Editar Usuario", command=editar_usuario)
editar_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="WE")

eliminar_button = tk.Button(root, text="Eliminar Usuario", command=eliminar_usuario)
eliminar_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="WE")

usuarios_listbox = tk.Listbox(root, height=10, width=50)
usuarios_listbox.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
usuarios_listbox.bind('<<ListboxSelect>>', seleccionar_usuario)

# Mostrar usuarios al iniciar la aplicación
mostrar_usuarios()

root.mainloop()