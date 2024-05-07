from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

# Crear un entorno de Jinja2
env = Environment(loader=FileSystemLoader('.'))

# Cargar la plantilla HTML
template = env.get_template('plantilla_factura.html')

# Solicitar los datos de la factura al usuario
dayIssue = input("Ingrese el día de la emision (Únicamente el día, sin mes ni año): ")
monthIssue = input("Ingrese el mes de emisión: ")
yearIssue = input("Ingrese el año de emisión: ")


dateIssue = dayIssue + monthIssue + yearIssue

expirationDay = input("Ingrese el día de vencimiento: ")
monthExpiration = input("Ingrese el mes de vencimiento: ")
yearExpiration = input("Ingrese el año de vencimiento: ")



cliente = input("Ingrese el nombre del cliente: ")
servicio = input("Ingrese el nombre del servicio a cobrar: ")
while True:
    try:
        precioUnitario = int(input("Ingrese el precio unitario:"))
        cantidad = int(input("Ingrese la cantidad de unidades a cobrar: "))
        break
    except ValueError:
        print("Solo puede ingresar números")

total = precioUnitario * cantidad



# Renderizar la plantilla con los datos de la factura
html_content = template.render(dayIssue = dayIssue, monthIssue = monthIssue, yearIssue = yearIssue, cliente=cliente,cantidad=cantidad,servicio=servicio,precioUnitario=precioUnitario, total=total)

# Generar el nombre del archivo HTML y PDF
nombre_archivo = f"factura_{cliente}_{dateIssue}.html"
nombre_pdf = f"factura_{cliente}_{dateIssue}.pdf"

# Guardar el contenido HTML en un archivo
with open(nombre_archivo, 'w') as file:
    file.write(html_content)

# Convertir el archivo HTML a PDF
HTML(nombre_archivo).write_pdf(nombre_pdf)

print(f"La factura se ha generado exitosamente.")
print(f"Archivo HTML: {nombre_archivo}")
print(f"Archivo PDF: {nombre_pdf}") 