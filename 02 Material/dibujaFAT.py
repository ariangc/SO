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


fatType = "FAT32"
dataStart = 0

with open(sys.argv[1], "rb") as fimage:
    #Revisamos el tipo de FAT de la imagen proporcionada
    fimage.seek(54)
    entry = fimage.read(8)
    entry = str(entry)[2:7]

    if entry == "FAT16":
        fatType = "FAT16"

    print(fatType)

    if fatType == "FAT32":
        fimage.seek(14)
        numReserved = fimage.read(2)
        numReserved = int.from_bytes(numReserved,byteorder='little')

        fimage.seek(11)
        bytesPerSect = fimage.read(2)
        bytesPerSect = int.from_bytes(bytesPerSect, byteorder='little')

        dataStart = bytesPerSect * numReserved
        print(dataStart)
    else:
        fimage.seek(14)
        numReserved = fimage.read(2)
        numReserved = int.from_bytes(numReserved,byteorder='little')

        fimage.seek(11)
        bytesPerSect = fimage.read(2)
        bytesPerSect = int.from_bytes(bytesPerSect, byteorder='little')
        dataStart = bytesPerSect * numReserved

with open(sys.argv[1],"rb") as fimage:
    fimage.seek(dataStart)
    print()
    for x in range(20):
        for y in range(20):
            entry = fimage.read(2 if fatType == "FAT16" else 4)
            i = int.from_bytes(entry,byteorder='little')
            #print(i)
            if x == 0 and y == 0:
                grid[x][y] = (2,"R")
            elif x == 0 and y == 1:
                grid[x][y] = (2,"R")
            elif i == (0xFFFF if fatType == "FAT16" else 0x0FFFFFFF):
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
