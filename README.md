La aplicación está alojada en un servidor Bluemix, de IBM.

Se puede ejecutar de forma local, siempre que se tenga instalado los siguientes módulos de Python:
- Flask
- Pymongo
- Bson

El servidor de la base de datos es el externo, y está identificado en la línea 16 del archivo index.py. Cuando el archivo no se ejecuta de forma local, y se ejecuta en el servidor, hay que descomentar las líneas 11, 12 y 14, y comentar la línea 16.
