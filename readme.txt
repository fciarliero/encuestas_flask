******************pasos para instalar*******************
instalar docker https://www.docker.com/get-started
abrir una terminal de powershell en alguna carpeta 
y ejecutar: 
"git clone https://github.com/fciarliero/encuestas_flask.git"
"cd encuestas_flask"
"docker-compose up --build"


********************comentarios**************************
la aplicacion deberia estar corriendo en http://localhost:5000/
notar que no es un deploy para produccion sino que es para desarrollo

lo mas desafiante para mi de este proyecto fue determinar que schema
usar para la base de datos de manera que sea escalable y que pueda
cumplir con todos los requisitos por mas que no los tenga implementados
en ese momento.

lo segundo mas complicado fue aprender todas las cosas que nunca use antes,
como docker, sqlalchemy o el modulo flask-login. no necesariamente porque
hayan sido cosas dificiles de aprender, sino porque al momento de arrancar 
uno no sabe cuan profundo es el agujero de conejo de cada uno de esos temas.


**********************cosas que faltan********************
*un frontend
*hacer tests
*poder ver los resultados de las encuestas
*poder buscar encuestas mediante tags
*ver las encuestas generadas por cada usuario
*ver las respuestas generadas por cada usuario
*utilizar algun servidor tipo waitress en vez del de desarrollo de flask
*cambiar la SECRET_KEY 
