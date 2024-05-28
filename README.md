Proyecto 3er Parcial
Este proyecto consiste en un sistema distribuido para la generación y consumo de mensajes utilizando Docker y Python.

Contenido del Proyecto
docker-compose.yml: Archivo de configuración de Docker Compose para gestionar los servicios del proyecto.
grafics.py: Script en Python para la generación de gráficos.
message_consumer.py: Script en Python para consumir mensajes de una cola.
message_generator.py: Script en Python para generar y enviar mensajes a una cola.
myenv: Entorno virtual de Python con las dependencias necesarias.
Requisitos
Docker y Docker Compose instalados en el sistema.
Python 3.x
Configuración y Ejecución
1. Clonar el repositorio
Clona el repositorio a tu máquina local:

bash
Copy code
git clone <URL_DEL_REPOSITORIO>
cd proyecto3erparcial
2. Configurar el entorno virtual
Si el entorno virtual (myenv) no está configurado, crea y activa uno nuevo:

bash
Copy code
python3 -m venv myenv
source myenv/bin/activate  # En Windows usa `myenv\Scripts\activate`
Instala las dependencias necesarias:

bash
Copy code
pip install -r requirements.txt
3. Ejecutar con Docker Compose
Levanta los servicios definidos en docker-compose.yml:

bash
Copy code
docker-compose up
Este comando iniciará los contenedores necesarios para el proyecto.

Scripts
1. message_generator.py
Este script genera y envía mensajes a una cola.

Ejecución:

bash
Copy code
python message_generator.py
2. message_consumer.py
Este script consume mensajes de una cola y los procesa.

Ejecución:

bash
Copy code
python message_consumer.py
3. grafics.py
Este script genera gráficos basados en los datos procesados.

Ejecución:

bash
Copy code
python grafics.py
Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que desees realizar.

Licencia
Este proyecto está licenciado bajo los términos de la MIT License.
