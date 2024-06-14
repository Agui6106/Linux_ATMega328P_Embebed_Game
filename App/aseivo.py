# - Aseivo game - #

import pygame, sys, random
import time

pygame.init()
pygame.display.set_caption("Aseivo Game")

negro = (0,0,0)
verde=(22,160,133)
blanco = (236,240,241)
rojo = (176,58,46)
azul = (36,113,163)

colores=[negro,verde,rojo,azul]

size=(500,700)
screen=pygame.display.set_mode(size)
clock=pygame.time.Clock()

#pygame.display.set_caption("vidas=")
#Configurar la fuente typografica
font = pygame.font.Font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)  # Puedes ajustar el tamaño de la fuente aquí

#Configurar el color del texto
text_color = (0, 0, 0)  #Blanco en formato RGB

# Variables para controlar el parpadeo del texto
parpadeo_tiempo = time.time()
parpadeo_intervalo = 0.5  # Parpadear cada 0.5 segundos
texto_visible = True

#Variable para controlar el estado del juego
juego_finalizado = False
juego_ganado = False

coor_x=250
vel_x=0

x1=15
y1=-700
b=4
vidas=5
puntaje=0

#lista de colores
coloresB=[] 
x=[]  #lista posiciones x
y=[]  #lista posiciones y
#colores random
for i in range(b):
    coloresB.append(i)

    x.append(x1)
    y.append(y1)
    x1=random.randint(10,490)
    y1+=200

pantalla_inicio = True

while True:

    while pantalla_inicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pantalla_inicio = False

        # Superponer una pantalla negra
        screen.fill((0, 0, 0))  # Rellenar con negro la pantalla

        # Crear un objeto de texto
        textInicio = font.render("Star", True, blanco)

        # Obtener el rectángulo del texto
        textInicio_rect = textInicio.get_rect()
        # Posicionar el texto
        textInicio_rect.center = (500 // 2, 700 // 2)  # Posicionar el texto en el centro del la pantalla
        # Dibujar el texto en la pantalla
        screen.blit(textInicio, textInicio_rect)

        pygame.display.flip()

    def mover_derecha():
        coor_x+=vel_x
    for event in pygame.event.get():
        #print(event)
        #movimiento horizonal
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and (juego_finalizado == True or juego_ganado == True):
                # Si el jugador presiona la tecla ESPACIO mientras el juego no está finalizado, reinicia el juego
                puntaje = 0
                vidas = 5

                x1=15
                y1=-700
                #lista de colores
                coloresB=[] 
                x=[]  #lista posiciones x
                y=[]  #lista posiciones y
                #colores random
                for i in range(b):
                    coloresB.append(i)

                    x.append(x1)
                    y.append(y1)
                    x1=random.randint(10,490)
                    y1+=200
                juego_finalizado = False
                juego_ganado = False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_d: 
                vel_x=6
            if event.key==pygame.K_a:
                vel_x=-6
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_d:
                vel_x=0
            if event.key==pygame.K_a:
                vel_x=0

    screen.fill(blanco)

    #zona de programacion 
    if coor_x>470:
        coor_x=0
    if coor_x<0:
        coor_x=470
    coor_x+=vel_x
    if vidas <= 0:
        juego_finalizado = True
    if puntaje >= 30:
        juego_ganado = True

    if juego_finalizado == False and juego_ganado == False:
        #zona de dibujo 
        mono=pygame.draw.rect(screen,rojo,[coor_x,600,30,30])
        
        for j in range(b):  
            platanos=pygame.draw.circle(screen, coloresB[j], (x[j], y[j]), 10)

            y[j]+=3  #animacion

            if mono.colliderect (platanos):
                y[j]=0  #nueva posición en y
                x[j]=random.randint(10,490) #nueva posición en x
                coloresB[j]=colores[random.randint(0,3)]  #nuevo colorS
                puntaje+=1

            #si la bola llega al final, reiniciar su posición en Y y cambiar su color
            if y[j]>size[1] and mono.colliderect (platanos) == False:
                y[j]=0  #nueva posición en y
                x[j]=random.randint(10,490) #nueva posición en x
                coloresB[j]=colores[random.randint(0,3)]
                vidas-=1
    

    if juego_finalizado:
        #Superponer una pantalla negra
        screen.fill((0, 0, 0))  #Rellenar con negro la pantalla

        #Crear un objeto de texto
        text = font.render("Game Over", True, blanco)

        #Obtener el rectángulo del texto
        text_rect = text.get_rect()
        #Posicionar el texto
        text_rect.center = (500 // 2, 700 // 2) #Pocisionar el texto en el centro del la pantalla
        #Dibujar el texto en la pantalla
        screen.blit(text, text_rect)
        
        # Verificar el parpadeo del texto cada 2 segundos
        tiempo_actual = time.time()
        if tiempo_actual - parpadeo_tiempo >= parpadeo_intervalo:
            parpadeo_tiempo = tiempo_actual
            texto_visible = not texto_visible

        if texto_visible:
            #Crear un objeto de texto
            textReinicio = font.render("Presione ENTER", True, blanco)

            #Obtener el rectángulo del texto
            text_rectReinicio = textReinicio.get_rect()
            text_rectReinicio.center = (500 // 2, (700 // 2) - 100) #Pocisionar el texto en el centro del la pantalla
            #Dibujar el texto en la pantalla
            screen.blit(textReinicio, text_rectReinicio)

    elif puntaje >= 30 and juego_ganado:
        #Superponer una pantalla negra
        screen.fill((0, 0, 0))  #Rellenar con negro la pantalla

        #Crear un objeto de texto
        text = font.render("Ganaste", True, blanco)

        #Obtener el rectángulo del texto
        text_rect = text.get_rect()
        #Posicionar el texto
        text_rect.center = (500 // 2, 700 // 2) #Pocisionar el texto en el centro del la pantalla
        #Dibujar el texto en la pantalla
        screen.blit(text, text_rect)
        
        # Verificar el parpadeo del texto cada 2 segundos
        tiempo_actual = time.time()
        if tiempo_actual - parpadeo_tiempo >= parpadeo_intervalo:
            parpadeo_tiempo = tiempo_actual
            texto_visible = not texto_visible

        if texto_visible:
            #Crear un objeto de texto
            textReinicio = font.render("Presione ENTER", True, blanco)

            #Obtener el rectángulo del texto
            text_rectReinicio = textReinicio.get_rect()
            text_rectReinicio.center = (500 // 2, (700 // 2) - 100) #Pocisionar el texto en el centro del la pantalla
            #Dibujar el texto en la pantalla
            screen.blit(textReinicio, text_rectReinicio)

    else:
        textVida = font.render(f"Vidas: {vidas}", True, text_color)

        textPuntaje = font.render(f"Puntaje: {puntaje}", True, text_color)
        #Obtener el rectángulo del texto
        text_rectVida = textVida.get_rect()
        text_rectPuntaje = textPuntaje.get_rect()

        #Posicionar el texto
        text_rectVida.center = (50, 25) #Pocisionar el texto
        text_rectPuntaje.center = (450, 25) #Pocisionar el texto

        #Dibujar el texto en la pantalla
        screen.blit(textVida, text_rectVida)
        screen.blit(textPuntaje, text_rectPuntaje)


    
    pygame.display.flip()
    clock.tick(60)