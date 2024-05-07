import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style, DateEntry
from jinja2 import Environment, FileSystemLoader
from fpdf import FPDF
import os

def abrir_seccion_clientes():
    # Lógica para abrir la sección de clientes
    print("Abriendo sección de clientes...")

def generar_factura():
    # Obtener los valores de los campos de entrada
    dayIssue = calendar_issue.entry.get()
    monthIssue = calendar_issue.entry.get()
    yearIssue = calendar_issue.entry.get()
    dateIssue = calendar_issue.entry.get().replace("/", "")
    expirationDay = calendar_expiration.entry.get()
    monthExpiration = calendar_expiration.entry.get()
    yearExpiration = calendar_expiration.entry.get()
    cliente = entry_cliente.get()
    servicio = entry_servicio.get()
    precioUnitario = int(entry_precioUnitario.get())
    cantidad = int(entry_cantidad.get())
    total = precioUnitario * cantidad

    # Crear un entorno de Jinja2
    env = Environment(loader=FileSystemLoader('.'))
    
    # Cargar la plantilla HTML
    template = env.get_template('plantilla_factura.html')
    
    # Renderizar la plantilla con los datos de la factura
    html_content = template.render(dayIssue=dayIssue, monthIssue=monthIssue, yearIssue=yearIssue, cliente=cliente,
                                   cantidad=cantidad, servicio=servicio, precioUnitario=precioUnitario, total=total)

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
    pdf.cell(30, 10, txt=str(precioUnitario), border=1)
    pdf.cell(30, 10, txt=str(total), border=1, ln=1)

    pdf.cell(200, 10, txt="", ln=1)
    pdf.cell(200, 10, txt=f"Total: {total}", ln=1, align="R")

    # Guardar el PDF
    pdf.output(nombre_pdf)

    print(f"La factura se ha generado exitosamente.")
    print(f"Archivo HTML: {nombre_archivo}")
    print(f"Archivo PDF: {nombre_pdf}")

# Crear la ventana principal
window = tk.Tk()
window.title("Generador de Facturas")
window.geometry("500x600")

# Aplicar el estilo Daisy UI oscuro y azul
style = Style(theme="darkly")
style.configure(".", background="#121212", foreground="white", font=("Arial", 12))
style.configure("TLabel", background="#121212", foreground="white")
style.configure("TButton", background="#2196F3", foreground="white")
style.configure("TEntry", fieldbackground="#1F1F1F", foreground="white")

# Crear un contenedor con barra de desplazamiento
container = ttk.Frame(window)
canvas = tk.Canvas(container, bg="#121212")
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas, style="TFrame")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

container.pack(fill="both", expand=True)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Cargar y mostrar el logo
logo_image = tk.PhotoImage(file="/logo.png")
logo_label = ttk.Label(scrollable_frame, image=logo_image, background="#121212")
logo_label.pack(pady=20)

# Crear los campos de entrada
label_cliente = ttk.Label(scrollable_frame, text="Nombre del cliente:")
label_cliente.pack()
entry_cliente = ttk.Entry(scrollable_frame)
entry_cliente.pack()

label_servicio = ttk.Label(scrollable_frame, text="Nombre del servicio:")
label_servicio.pack()
entry_servicio = ttk.Entry(scrollable_frame)
entry_servicio.pack()

label_precioUnitario = ttk.Label(scrollable_frame, text="Precio unitario:")
label_precioUnitario.pack()
entry_precioUnitario = ttk.Entry(scrollable_frame)
entry_precioUnitario.pack()

label_cantidad = ttk.Label(scrollable_frame, text="Cantidad:")
label_cantidad.pack()
entry_cantidad = ttk.Entry(scrollable_frame)
entry_cantidad.pack()

label_issue_date = ttk.Label(scrollable_frame, text="Fecha de emisión:")
label_issue_date.pack()
calendar_issue = DateEntry(scrollable_frame, width=12, dateformat="%d/%m/%Y")
calendar_issue.pack()

label_expiration_date = ttk.Label(scrollable_frame, text="Fecha de vencimiento:")
label_expiration_date.pack()
calendar_expiration = DateEntry(scrollable_frame, width=12, dateformat="%d/%m/%Y")
calendar_expiration.pack()

# Crear el botón de generar factura
button_generar = ttk.Button(scrollable_frame, text="Generar Factura", command=generar_factura, style="TButton")
button_generar.pack(pady=20)

# Crear el botón para abrir la sección de clientes
button_clientes = ttk.Button(scrollable_frame, text="Clientes", command=abrir_seccion_clientes, style="TButton")
button_clientes.pack()

# Centrar los elementos en la ventana
for widget in scrollable_frame.winfo_children():
    widget.pack_configure(anchor="center")

# Ejecutar la ventana principal
window.mainloop()