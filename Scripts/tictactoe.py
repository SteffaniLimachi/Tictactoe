import copy
import sys
import pygame
import random
import numpy as np

from constants import *

# --- PYGAME SETUP ---

pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT_N) )
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill( BG_COLOR )
# --- CLASSES ---

class Board:

    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )
        self.empty_sqrs = self.squares # [squares]
        self.marked_sqrs = 0

    def final_state(self, show=False):
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''

        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # no win yet
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append( (row, col) )
        
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0
    
    def eval_reset(self):
        final_state = self.final_state(show=False)
        if final_state in [1, 2] or self.isfull():
            return True, final_state
        else:
            return False, None


class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # --- RANDOM ---

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (row, col)

    # --- MINIMAX ---

    def minimax(self, board, maximizing):
        
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # --- MAIN EVAL ---

    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move # row, col
    

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1   #1-cross  #2-circles
        self.gamemode = 'ai' # pvp or ai
        self.running = True
        self.show_lines()

    # --- DRAW METHODS ---

    def show_lines(self):
        # bg
        screen.fill( BG_COLOR )

        try:
            background_image = pygame.image.load('images/Logo_D4G.png').convert_alpha()
        except pygame.error as e:
            print(f'Error al cargar la imagen: {e}')
            sys.exit()

        # Ajustar el tamaño de la imagen al tamaño de la ventana, si es necesario
        background_image = pygame.transform.scale(background_image, (600, 97))

        # Dibujar la imagen en la ventana
        screen.blit(background_image, (WIDTH-600, 700-97))

        # vertical
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw cross
            # desc line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            # asc line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
        
        elif self.player == 2:
            # draw circle
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    # --- OTHER METHODS ---

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():

    # --- OBJECTS ---

    game = Game()
    board = game.board
    ai = game.ai
    counter = 0
    

    # --- MAINLOOP ---
    while True:
        # pygame events
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # keydown event
            if event.type == pygame.KEYDOWN:

                # g-gamemode
                #if event.key == pygame.K_g:
                #    game.change_gamemode()

                # r-restart

                if (event.key == pygame.K_r):
                    game.reset()
                    board = game.board
                    ai = game.ai

                # 0-random ai
                #if event.key == pygame.K_0:
                #    ai.level = 0
                
                # 1-random ai
                #if event.key == pygame.K_1:
                #    ai.level = 1

            # click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                
                # human mark sqr
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False

        #print(board.eval_reset())
        #if board.eval_reset():
        #    pygame.display.update()
        #    game.reset()    
        #    board = game.board
        #    ai = game.ai
                        
        # Al final del bucle principal, después de toda la lógica de eventos y actualizaciones
        reset, winner = board.eval_reset()
        if reset:
            if winner == 1:
                message = "GANADOR: JUGADOR 1!"
            elif winner == 2:
                message = "GANADOR: JUGADOR 2!"
            else:
                message = "EMPATE!"
            
            # Preparar el mensaje para mostrar
            pygame.display.update()

            screen.fill( WHITE )


            # Ajustar el tamaño de la imagen al tamaño de la ventana, si es necesario
            background_image = pygame.image.load('images/Logo_D4G_1.png').convert_alpha()
            background_image = pygame.transform.scale(background_image, (330, 250))
            screen.blit(background_image, (WIDTH-350, HEIGHT_N-300))

            background_image1 = pygame.image.load('images/LOGO_DATEC_NEGRO.png').convert_alpha()
            background_image1 = pygame.transform.scale(background_image1, (400, 150))
            screen.blit(background_image1, (50, 50))

            pygame.font.init()
            font_name = pygame.font.get_fonts()[5]  # Obtiene el nombre de la primera fuente disponible
            font = pygame.font.SysFont(font_name, 50)
            #font = pygame.font.Font(font, 70)
            text = font.render(message, True, (0, 0, 0), WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, (HEIGHT_N // 2)-20))
            
            # Dibujar el mensaje en la pantalla
            screen.blit(text, text_rect)
            pygame.display.update()
            # Esperar unos segundos
            pygame.time.wait(1000)
            
            # Reiniciar el juego
            game.reset()
            board = game.board
            ai = game.ai

            if (counter % 4 == 0):
                ai.level = 0
                print(counter)
            else:
                ai.level = 1
            counter+=1

        # AI initial call
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            
            # update the screen
            pygame.display.update()

            # eval
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False
            
        pygame.display.update()

main()