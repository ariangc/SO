"""
 Programa que muestra el Boot Sector de la FAT
 Prof. A. Bello
 Pontificia Universidad Católica del Perú
"""
import sys
import pygame

# Definimos algunos colores

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = ( 0, 255, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
CIAN = (0, 255, 255)
MAGNETA = (255, 0, 255)

# Establecemos el LARGO y ALTO de la fila
LARGO  = 400
ALTO = 25

# Establecemos el margen entre las celdas.
MARGEN = 3

fimage = open(sys.argv[1],"rb")

#Contenido del Boot Sector, primeros 36 bytes
toffsets = [(3,"Código de máquina"), (8,"Identificador del fabricante"),\
            (2,"Bytes por sector"), (1,"Sectores por cluster"),\
            (2,"Sectores reservados"),(1,"Númeero de FAT's"),\
            (2,"Entrada máxima de directorio raíz"),(2,"Sectores totales"),\
            (1,"Descriptor de medio"),(2,"Sectores por FAT"),\
            (2,"Sectores por pista"), (2,"Número de caras"),\
            (4,"Sectores ocultos"), (4,"Longitud total de sectores")]

# Inicializamos pygame
pygame.init()

# Establecemos el LARGO y ALTO de la pantalla
DIMENSION_VENTANA = [405, 400]
pantalla = pygame.display.set_mode(DIMENSION_VENTANA)

# Establecemos el título de la pantalla.
pygame.display.set_caption("Boot Sctor FAT")

# Iteramos hasta que el usuario pulse el botón de salir.
hecho = False

# Lo usamos para establecer cuán rápido de refresca la pantalla.
reloj = pygame.time.Clock()

fuente = pygame.font.Font(None, 25)




# -------- Bucle Principal del Programa-----------
while not hecho:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            hecho = True
    # Establecemos el fondo de pantalla.
    pantalla.fill(NEGRO)

    # Dibujamos las filas
    color = AMARILLO
    for fila in range(14):
            pygame.draw.rect(pantalla,
                             color,
                             [ MARGEN,
                              (MARGEN+ALTO) * fila + MARGEN,
                              LARGO,
                              ALTO])

    fila = 0
    fimage.seek(0)
    #Imprimimos texto y contenido del Boot sector
    for (offset,texto) in toffsets:
        entry = fimage.read(offset)
        if fila == 1:
            entry = entry.decode()
            texto = texto + " : " + entry
        else:
            entry = int.from_bytes(entry,byteorder='little')
            texto = texto + " : " + str(entry)
        texto1 = fuente.render(texto, 0, (0, 0, 0))
        pantalla.blit(texto1, (MARGEN+4,(MARGEN+ALTO)*fila + MARGEN + 5))
        fila += 1

    # Limitamos a 60 fotogramas por segundo.
    reloj.tick(60)

    # Avanzamos y actualizamos la pantalla con lo que hemos dibujado.
    pygame.display.flip()

# Pórtate bien con el IDLE.
fimage.close()
pygame.quit()
