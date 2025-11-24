INVENTABLE – Sistema Web para Gestión de Restaurantes
=====================================================

Este directorio contiene los archivos fuente del proyecto desarrollado en Django 
para la asignatura Electiva Ciencia de Datos. El sistema permite gestionar reservas 
de mesas, pedidos y generar reportes básicos de ventas.

CONTENIDO DEL DIRECTORIO
------------------------
El directorio incluye:

- manage.py
- inventable/  (configuración del proyecto)
- clientes/    (módulo para gestión de clientes)
- reservas/    (módulo para creación de reservas)
- pedidos/     (módulo de gestión de pedidos)
- menu/        (módulo donde se registran los productos)
- usuarios/    (módulo de gestión de empleados/usuarios)
- db.sqlite3   (base de datos con las tablas y estructura del proyecto)

REQUISITOS DEL SISTEMA
----------------------
Para ejecutar correctamente el proyecto se requiere:

- Python 3.10 o superior
- pip actualizado
- Django 5.2 o superior

Se recomienda crear un entorno virtual (venv).

INSTRUCCIONES DE INSTALACIÓN
----------------------------

1. Abrir la consola (PowerShell, CMD o terminal)
2. Navegar a la carpeta del proyecto:

   cd INVENTABLE

3. Crear un entorno virtual:

   python -m venv venv

4. Activar el entorno virtual:

   Windows:
   .\venv\Scripts\activate

5. Instalar dependencias:

   pip install django

6. Aplicar migraciones:

   python manage.py migrate

   (En caso de estar incluida la base de datos db.sqlite3, este paso ya viene configurado.)

7. Crear un superusuario:

   python manage.py createsuperuser

8. Ejecutar el servidor:

   python manage.py runserver

9. Abrir en el navegador:

   http://127.0.0.1:8000/

RUTAS PRINCIPALES DEL SISTEMA
------------------------------

- /admin           → Panel administrativo de Django
- /clientes/       → Gestión de clientes
- /reservas/       → Crear y administrar reservas
- /pedidos/        → Registrar pedidos por mesa
- /menu/           → Productos del menú

SOBRE EL PROYECTO
-----------------
Este proyecto implementa:

- Modelos de datos para clientes, productos, pedidos, reservas y usuarios.
- Formularios para creación y edición de registros.
- Vistas basadas en funciones.
- Sistema de reportes básicos.
- Base de datos SQLite3 lista para uso inmediato.

AUTORES
--------
Yuliet Sakura Garcia Fonseca – ysgarciaf@itc.edu.co  
Mia Alexandra Camacho Sanchez – macamachos@itc.edu.co  

Repositorio en GitHub:
https://github.com/Miaalexan/INVENTABLE.git

