"""
 Programa que muestra de forma gráficfa las primeras entradas de la FAT
 Prof. Alejandro T. Bello
 Pontificia Universidad Católica
"""
import sys
import pygame
import os
 
# Definimos algunos colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = ( 0, 255, 0)
ROJO = (255, 0, 0)
 
# Establecemos el LARGO y ALTO de cada celda de la retícula.
LARGO  = 30
ALTO = 30
 
# Establecemos el margen entre las celdas.
MARGEN = 5
 
# Creamos un array bidimensional. Un array bidimensional
# no es más que una lista de listas.
grid = []
for fila in range(20):
    # Añadimos un array vacío que contendrá cada celda 
    # en esta fila
    grid.append([])
    for columna in range(20):
        grid[fila].append((0,0)) # Añade una celda
 

with open(sys.argv[1],"rb") as fimage:
    t1 = fimage.read(2)
    t2 = fimage.read(2)
    t1 = int.from_bytes(t1, byteorder='little')
    t2 = int.from_bytes(t2, byteorder='little')
    print(str(t1),str(t2))
    fimage.seek(4096)
    for x in range(20):
        for y in range(20):
            entry = fimage.read(2)
            i = int.from_bytes(entry,byteorder='little')
            if x == 0 and y == 0:
                grid[x][y] = (2,"R")
            elif x == 0 and y == 1:
                grid[x][y] = (2,"R")
            elif i == 65535:                
                grid[x][y] = (1,"EOF")
            elif i != 0: 
                grid[x][y] = (1,str(i))
            else:    
                grid[x][y] = (0,str(i))
            
# Inicializamos pygame
pygame.init()
  
# Establecemos el LARGO y ALTO de la pantalla
DIMENSION_VENTANA = [705, 705]
pantalla = pygame.display.set_mode(DIMENSION_VENTANA)
 
# Establecemos el título de la pantalla.
pygame.display.set_caption("FAT")
 
# Iteramos hasta que el usuario pulse el botón de salir.
hecho = False
 
# Lo usamos para establecer cuán rápido de refresca la pantalla.
reloj = pygame.time.Clock()

fuente = pygame.font.Font(None, 21)
 
# -------- Bucle Principal del Programa-----------
while not hecho:
    for evento in pygame.event.get(): 
        if evento.type == pygame.QUIT: 
            hecho = True       
    # Establecemos el fondo de pantalla.
    pantalla.fill(NEGRO)
        
    # Dibujamos la FAT
    for fila in range(20):
        for columna in range(20):
            #print(fila,columna)            
            color = BLANCO
            if (grid[fila][columna])[0] == 1:
                color = VERDE                
            if (grid[fila][columna])[0] == 2:
                color = ROJO                
            X = (MARGEN+LARGO) * columna + MARGEN
            Y = (MARGEN+ALTO) * fila + MARGEN
            pygame.draw.rect(pantalla,color,[X,Y,LARGO,ALTO])
            
            t = (grid[fila][columna])[1]            
            texto1 = fuente.render(t, 0, (0, 0, 0))
            pantalla.blit(texto1,(X,Y+5))  
            
    # Limitamos a 60 fotogramas por segundo.
    reloj.tick(60)
 
    # Avanzamos y actualizamos la pantalla con lo que hemos dibujado.
    pygame.display.flip()
     
fimage.close()
pygame.quit()
