# Drobots
Práctica final para la asignatura de Sistemas Distribuidos de la UCLM.
### Tecnologías

 - ZeroC Ice 3.6 (IceGrid e IcePatch2)
 - Python 3.x
 - Java 8
## Contenido
La práctica contiene 3 aplicaciones de IceGrid
 - **La primera**, *icegridApp.xml*: Existe con fines de depuración, es una aplicación donde solo se necesita un nodo para ejecutar la aplicación (preferiblemente Linux), **hace uso** de plantillas
 - **La segunda**, *icegridAppWin*: Una aplicación donde un nodo (el tercero) está en otra máquina Windows, **no hace uso** de plantillas.
 - **La tercera (y principal)**, *icegridAppWinPlantilla.xml*: Combina las 2 aplicaciones anteriores, **hace uso** de plantillas y otro nodo está distribuido en otra máquina Windows (nodo 3). **La única aplicación a ser ejecutada**

## Uso
### Rutas y runtime de Ice
Para la correcta ejecución de la práctica hacen falta modificar algunas propiedades de la práctica ya que estos valores son diferentes en cada instalación de Ice
 - **Localización del runtime de Ice** en el Makefile, variable *CLASSPATH* para la correcta compilación del codigo java
 - **Localización del runtime de Ice** en *GameMaster.py*, en la línea *Ice.loadSlice* para la correcta compilación en runtime del slice del game observer
 - **Localización del runtime de Ice** en el servidor *DetectorFactory, nodo 2*, en la propiedad *Command Arguments* para la correcta ejecución del servidor
 - **Localización del ejecutable python** en los servidores *game_observer* y *Robot_Factory3*, en el parámetro *executable*. **Solo necesario si estamos ejecutando ese nodo en Windows**
 - **IP del registry**, en la configuración del nodo3, en la propiedad *Ice.Default.Locator*. **Solo en Windows**
 - **IP del registry**, en la primera linea del script start.sh, se pondra la ip de la maquina que ejecute el nodo1 (el registry)
 - **Carpeta de datos del nodo3**, en la configuración del nodo3, en la propiedad *IceGrid.Node.Data*. ** Solo en Windows**
 - **Nombre del jugador** y **Nombre de la partida**, en las propiedades del servidor *Player*

### Comandos
 La práctica tiene un Makefile que hace que la ejecución de la práctica sea semiautomática.
 **A ejecutar en Linux**
 Lista de objetivos del Makefile:
 - **start-grid**: Inicia el registry, locator y los 2 nodos pertenecientes al entorno Linux.
 - **compile**: Copia los archivos *.py*, *.ice* a la carpeta *build*, compila el código Java, lo guarda y ejecuta *icepatch2calc*
 - **update**: Copia los archivos *.py*, *.ice* a la carpeta *build*, **no** compila código Java y ejecuta *icepatch2calc*
 - **start-script**: Inicia todos los servidores de la aplicación, previamente es **necesario** haber guardado la aplicación al registry
 - **stop-script**: Para todos los servidores de la aplicación activa en el registry.
**A ejecutar en Windows**
En Windows no es necesario el uso de un Makefile debido a que solo es necesario el uso de un solo comando (en Powershell):
    icegridnode --Ice.Config=node3.config
### Ejecución
 Una vez cambiados los parámetros citados en la sección *Rutas y runtime de Ice* los pasos necesarios para ejecutar la aplicación son:
 **En Linux**
 - Ejecutar: *make*  Esto iniciará el grid necesario en linux y compilará todo el código necesario
 - Abrir la aplicación icegridgui, abrir la aplicación *icegridAppWinPlantilla.xml* y guardarla en el registry.
 **En Windows**
 - Ejecutar: *icegridnode --Ice.Config=node3.config*
 **En Linux**
 - Ejecutar: *make start-script*
