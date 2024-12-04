#!/bin/bash

# Mover al directorio del proyecto si es necesario
cd Producto/renta_hogar

# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

# Cargar datos iniciales
python manage.py loaddata populate_data.json

# Iniciar el servidor Django
python manage.py runserver
