import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configurar la ventana de visualización
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Ejemplo de Imagen con Pygame')

# Cargar la imagen de fondo
# Asegúrate de reemplazar 'nombre_de_tu_imagen.png' con el nombre de tu archivo de imagen PNG
try:
    background_image = pygame.image.load('Logo_D4G.png').convert_alpha()
    print('Hola')   
except pygame.error as e:
    print(f'Error al cargar la imagen: {e}')
    sys.exit()

# Ajustar el tamaño de la imagen al tamaño de la ventana, si es necesario
background_image = pygame.transform.scale(background_image, (width, height))

# Dibujar la imagen en la ventana
screen.blit(background_image, (0, 0))

# Actualizar la ventana de visualización para mostrar la imagen
pygame.display.update()

# Bucle para mantener la ventana abierta
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
