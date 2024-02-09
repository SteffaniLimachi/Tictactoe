import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Configuraciones de pantalla
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Configuración de fuente
font = pygame.font.Font(None, 36)

# Opciones del menú
menu_items = ['Jugar', 'Salir']
selected_item = 0

def draw_menu():
    screen.fill(BLACK)  # Fondo del menú
    for index, item in enumerate(menu_items):
        if index == selected_item:
            color = RED  # Resalta la opción seleccionada
        else:
            color = WHITE
        text = font.render(item, True, color)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 20 + 40 * index))

def main():
    global selected_item
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if selected_item == 0:
                        print("Jugar seleccionado")  # Aquí inicia el juego
                    elif selected_item == 1:
                        running = False  # Salir del juego

        draw_menu()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
