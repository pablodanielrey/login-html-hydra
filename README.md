# login-html-hydra

para poder ejecutar el sistema para poder desarrollar
se debe usar:
(debido al diseño de docker-compose usando run no te mapea los puertos, por lo que se debe ejecutar usando up)


cd raiz-del-proyecto
docker-compose build
docker-compose up

ahora se puede ejecutar un shell dentro del proyecto y poder correrlo.

docker exec -ti contenedor bash
cd /src
bash instalar.sh

y ejecutar el sistema

python -m login_html_hydra

a partir de ahí se puede acceder al link

http://localhost:10005


-----

para ejecutar los testings desde la raiz activar el environment usando:

source env/bin/activate

y despues ejecutar los tests desde la raiz del proyecto usando:

pytest

se pueden ejecutar los tests sobre el ambiente de producción usando 

pytest --environ prod 

previante hay que generar los portforwardings usando.

servicios/oidc/scripts/generar-port-forwarding-para-login.sh


