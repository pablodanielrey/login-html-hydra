# login-html-hydra

para poder ejecutar el sistema para poder desarrollar
se debe usar:


-- primero levantamos servicios básicos necesarios para la ejecución --

cd raiz-del-proyecto/tests/containers
docker-compose build
docker-compose up 

---- y en otra terminal ejecutamos el sistema ----

cd raiz-del-proyecto
docker-compose build
docker-compose up

a partir de ahí se puede acceder al link

http://localhost:10005


----- casos de testings ----

existen 2 entornos confogirados:

dev ---> 
el entorno de testing usa los contenedores internos tests/containers/docker-compose.yml
en este entorno se inserta un usuario de testeo

prod --->
el entorno de testing usa el contendor solamente de hydra-mock pero los accesos a las bases 
son mediante fortporwarding hacia los datos de producción.
esto permite ejeuctar los tests sobre el código actual pero utilizando datos de producción.


desde la raiz se puede usar pytest para ejecutar los tests.
(en el caso de que se use un virtual env separado se debe activar.)

source env/bin/activate

y despues ejecutar los tests desde la raiz del proyecto usando:

pytest

se pueden ejecutar los tests sobre el ambiente de producción usando 

pytest --environ prod 

previante hay que generar los portforwardings usando.

servicios/oidc/scripts/generar-port-forwarding-para-login.sh


------- Pasaje a producción -------


para generar la imagen que va a producción se usa el script 

build-prod.sh

utiliza el dockerfile que se encuentra dentro de docker/prod
instala gunicorn y usa eso para servir el sistema

