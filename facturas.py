import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style, DateEntry
from jinja2 import Environment, FileSystemLoader
from fpdf import FPDF
import os


def guardar_cliente():
    cliente = entry_cliente_seccion.get()
    servicio = entry_servicio_seccion.get()
    fecha_vencimiento = calendar_vencimiento_seccion.entry.get()
    precio_usd = entry_precio_seccion.get()

    if not cliente or not servicio or not fecha_vencimiento or not precio_usd:
        messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
        return
    
    # Guardar la información del cliente en la tabla
    tabla_clientes.insert("", "end", values=(cliente, servicio, fecha_vencimiento, precio_usd))
    
    # Limpiar los campos de entrada después de guardar
    entry_cliente_seccion.delete(0, "end")
    entry_servicio_seccion.delete(0, "end")
    calendar_vencimiento_seccion.entry.delete(0, "end")
    entry_precio_seccion.delete(0, "end")

    messagebox.showinfo("Cliente guardado", "El cliente se ha guardado correctamente.")

def actualizar_lista_clientes(*args):
    clientes = [tabla_clientes.item(item)['values'][0] for item in tabla_clientes.get_children()]
    entry_cliente['values'] = clientes


def mostrar_seccion_clientes():
    # Ocultar la sección de generación de facturas
    main_frame.pack_forget()
    
    # Mostrar la sección de clientes
    seccion_clientes_frame.pack(fill="both", expand=True)

def mostrar_seccion_facturacion():
    # Ocultar la sección de clientes
    seccion_clientes_frame.pack_forget()
    
    # Mostrar la sección de generación de facturas
    main_frame.pack(fill="both", expand=True)

def generar_factura():
    cliente = entry_cliente.get()
    servicio = entry_servicio.get()
    precio_unitario = entry_precioUnitario.get()
    cantidad = entry_cantidad.get()

    if not cliente or not servicio or not precio_unitario or not cantidad:
        messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
        return

    try:
        precio_unitario = int(precio_unitario)
        cantidad = int(cantidad)
    except ValueError:
        messagebox.showerror("Error", "Los campos de precio unitario y cantidad deben ser números.")
        return

    total = precio_unitario * cantidad

    dayIssue = calendar_issue.entry.get()
    monthIssue = calendar_issue.entry.get()
    yearIssue = calendar_issue.entry.get()
    dateIssue = calendar_issue.entry.get().replace("/", "")
    expirationDay = calendar_expiration.entry.get()
    monthExpiration = calendar_expiration.entry.get()
    yearExpiration = calendar_expiration.entry.get()

    # Crear un entorno de Jinja2
    env = Environment(loader=FileSystemLoader('.'))

    # Cargar la plantilla HTML
    template = env.get_template('plantilla_factura.html')

    # Renderizar la plantilla con los datos de la factura
    html_content = template.render(dayIssue=dayIssue, monthIssue=monthIssue, yearIssue=yearIssue, cliente=cliente,
                                   cantidad=cantidad, servicio=servicio, precioUnitario=precio_unitario, total=total)

    # Generar el nombre del archivo HTML y PDF
    nombre_archivo = f"factura_{cliente}_{dateIssue}.html"
    nombre_pdf = f"factura_{cliente}_{dateIssue}.pdf"

    # Guardar el contenido HTML en un archivo
    with open(nombre_archivo, 'w') as file:
        file.write(html_content)

    # Crear un objeto FPDF
    pdf = FPDF()
    pdf.add_page()

    # Agregar contenido al PDF
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Factura", ln=1, align="C")
    pdf.cell(200, 10, txt="", ln=1)

    pdf.cell(200, 10, txt=f"Fecha de emisión: {dayIssue}", ln=1)
    pdf.cell(200, 10, txt=f"Fecha de vencimiento: {expirationDay}", ln=1)
    pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=1)
    pdf.cell(200, 10, txt="", ln=1)

    pdf.cell(100, 10, txt="Servicio", border=1)
    pdf.cell(40, 10, txt="Cantidad", border=1)
    pdf.cell(30, 10, txt="Precio", border=1)
    pdf.cell(30, 10, txt="Total", border=1, ln=1)

    pdf.cell(100, 10, txt=servicio, border=1)
    pdf.cell(40, 10, txt=str(cantidad), border=1)
    pdf.cell(30, 10, txt=str(precio_unitario), border=1)
    pdf.cell(30, 10, txt=str(total), border=1, ln=1)

    pdf.cell(200, 10, txt="", ln=1)
    pdf.cell(200, 10, txt=f"Total: {total}", ln=1, align="R")

    # Guardar el PDF
    pdf.output(nombre_pdf)

    messagebox.showinfo("Factura generada", "La factura se ha generado correctamente.")

# Crear la ventana principal
window = tk.Tk()
window.title("Generador de Facturas")
window.geometry("800x600")  # Ajustar el tamaño de la ventana

# Aplicar el estilo Daisy UI oscuro y azul
style = Style(theme="darkly")
style.configure(".", background="#121212", foreground="white", font=("Arial", 12))
style.configure("TLabel", background="#121212", foreground="white")
style.configure("TButton", background="#2196F3", foreground="white")
style.configure("TEntry", fieldbackground="#1F1F1F", foreground="white", padding=5)
style.map("TEntry", fieldbackground=[("active", "#2A2A2A")])

# Crear un frame principal para la sección de generación de facturas
main_frame = ttk.Frame(window, style="TFrame")

# Cargar y mostrar el logo en la sección de generación de facturas
logo_image = tk.PhotoImage(file="logo.png")
logo_label = ttk.Label(main_frame, image=logo_image, background="#121212")
logo_label.configure(background="#121212")
logo_label.pack(pady=20)

# Crear un frame para los campos de entrada
entry_frame = ttk.Frame(main_frame, style="TFrame")
entry_frame.pack(pady=20)

# Crear los camposos de entrada
label_cliente = ttk.Label(entry_frame, text="Nombre del cliente:")
label_cliente.configure(background="#121212")  # Eliminar el fondo del label
label_cliente.pack()
entry_cliente = ttk.Entry(entry_frame, width=40)
entry_cliente.pack()

label_servicio = ttk.Label(entry_frame, text="Nombre del servicio:")
label_servicio.configure(background="#121212")  # Eliminar el fondo del label
label_servicio.pack()
entry_servicio = ttk.Entry(entry_frame, width=40)
entry_servicio.pack()

label_precioUnitario = ttk.Label(entry_frame, text="Precio unitario:")
label_precioUnitario.configure(background="#121212")  # Eliminar el fondo del label
label_precioUnitario.pack()
entry_precioUnitario = ttk.Entry(entry_frame, width=40)
entry_precioUnitario.pack()

label_cantidad = ttk.Label(entry_frame, text="Cantidad:")
label_cantidad.configure(background="#121212")  # Eliminar el fondo del label
label_cantidad.pack()
entry_cantidad = ttk.Entry(entry_frame, width=40)
entry_cantidad.pack()

label_issue_date = ttk.Label(entry_frame, text="Fecha de emisión:")
label_issue_date.configure(background="#121212")  # Eliminar el fondo del label
label_issue_date.pack()
calendar_issue = DateEntry(entry_frame, width=15, dateformat="%d/%m/%Y")
calendar_issue.pack()

label_expiration_date = ttk.Label(entry_frame, text="Fecha de vencimiento:")
label_expiration_date.configure(background="#121212")  # Eliminar el fondo del label
label_expiration_date.pack()
calendar_expiration = DateEntry(entry_frame, width=15, dateformat="%d/%m/%Y")
calendar_expiration.pack()

# Crear un frame para los botones
button_frame = ttk.Frame(main_frame, style="TFrame")
button_frame.pack(pady=20)

# Crear el botón de generar factura
button_generar = ttk.Button(button_frame, text="Generar Factura", command=mostrar_seccion_facturacion, style="TButton")
button_generar.pack(pady=10)

# Centrar los elementos en la ventana
main_frame.pack_configure(anchor="center")

# Crear un frame para la sección de clientes
seccion_clientes_frame = ttk.Frame(window, style="TFrame")

# Cargar y mostrar el logo en la sección de clientes
logo_clientes_label = ttk.Label(seccion_clientes_frame, image=logo_image, background="#121212")
logo_clientes_label.configure(background="#121212")
logo_clientes_label.pack(pady=20)

# Crear un frame para los campos de entrada de clientes
frame_clientes = ttk.Frame(seccion_clientes_frame, style="TFrame")
frame_clientes.pack(pady=20)

# Crear los campos de entrada de clientes
label_cliente_seccion = ttk.Label(frame_clientes, text="Nombre del cliente:")
label_cliente_seccion.configure(background="#121212")
label_cliente_seccion.pack()
entry_cliente_seccion = ttk.Entry(frame_clientes, width=40)
entry_cliente_seccion.pack()

label_servicio_seccion = ttk.Label(frame_clientes, text="Servicio:")
label_servicio_seccion.configure(background="#121212")
label_servicio_seccion.pack()
entry_servicio_seccion = ttk.Entry(frame_clientes, width=40)
entry_servicio_seccion.pack()

label_vencimiento_seccion = ttk.Label(frame_clientes, text="Fecha de vencimiento:")
label_vencimiento_seccion.configure(background="#121212")
label_vencimiento_seccion.pack()
calendar_vencimiento_seccion = DateEntry(frame_clientes, width=15, dateformat="%d/%m/%Y")
calendar_vencimiento_seccion.pack()

label_precio_seccion = ttk.Label(frame_clientes, text="Precio (USD):")
label_precio_seccion.configure(background="#121212")
label_precio_seccion.pack()
entry_precio_seccion = ttk.Entry(frame_clientes, width=40)
entry_precio_seccion.pack()

# Crear el botón para guardar la información del cliente
button_guardar_cliente = ttk.Button(frame_clientes, text="Guardar Cliente", command=guardar_cliente, style="TButton")
button_guardar_cliente.pack(pady=10)

# Crear una tabla para mostrar la información de los clientes
tabla_clientes = ttk.Treeview(seccion_clientes_frame, columns=("Cliente", "Servicio", "Fecha Vencimiento", "Precio (USD)"), show="headings")
tabla_clientes.heading("Cliente", text="Cliente")
tabla_clientes.heading("Servicio", text="Servicio")
tabla_clientes.heading("Fecha Vencimiento", text="Fecha Vencimiento")
tabla_clientes.heading("Precio (USD)", text="Precio (USD)")
tabla_clientes.pack(pady=20)

# Crear el botón para mostrar la sección de generación de facturas
button_facturacion = ttk.Button(seccion_clientes_frame, text="Generación de Facturas", command=mostrar_seccion_facturacion, style="TButton")
button_facturacion.pack()

# Crear el botón para mostrar la sección de clientes
button_clientes = ttk.Button(main_frame, text="Clientes", command=mostrar_seccion_clientes, style="TButton")
button_clientes.pack()

# Mostrar inicialmente la sección de generación de facturas
mostrar_seccion_facturacion()

# Ejecutar la ventana principal
window.mainloop()