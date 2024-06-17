# Linux_ATMega328P_Embedded_Game
Proyecto embebido con conexión serial Raspberry Pi - Microcontrolador ATMega328P Software (Diseño de Sistemas en Chip TE2003B)

Github complementario con la parte del Hardware: https://github.com/PaulinaLopezC/Control_ATmega328P_Embedded_Game


Se desarrollo un sistema embebido con la palca de desarrollo Raspberry Pi 4 y el microcontrolador ATMega328P para implementar una consola de videojuegos con comandos con nuestro control reflejado en nuestro videojuego. 

Para el desarrollo del software, se utiliza TKInter una librería de Python para desarrollar la interfaz gráfica de la aplicación, en esta  se implementaron 4 diferentes funciones estas son las siguientes: La configuración de conexión al control donde ajustamos el puerto y el Baudrate del control, así mismo hay un apartado donde se muestran los créditos correspondientes a los desarrolladores de los juegos por otra parte, la consola es capaz de registrar los scores más altos que el jugador obtenga en cada videojuego, así como la opción de subir estos datos a un servidor web programado por nosotros utilizando la librería FastAPI de Python. 

En el hardware se implementaron 2 microcontroladores para el control, porque requeríamos control de pantalla LCD y él envió datos de las entradas, como botones y joystick, y la recepción de datos enviados por nuestra aplicación para que nuestro control responda a estos comandos, esto mediante comunicación en serie para recibir y mandar datos en formato de comandos de 3 letras máximo.

Equipo 2:

Jose Alberto Aguilar Sanchez - A01735612

Guadalupe Paulina López Cuevas - A01701095

Jorge Israel Sandoval Sánchez - A01710373

4to Semestre IRS

## Créditos

El código del juego 1945 que se encunetra en la carpeta 1945 de este proyecto fue obtenido del repositorio [1945](https://github.com/sodacrunch/1945) creado por [sodacrunch](https://github.com/sodacrunch). Agradecemos al autor original por su excelente trabajo.
