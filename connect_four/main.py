import numpy as np
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7



# UTILITY FUNCTIONS
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece # i.e. added that value on that particular location


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
        

def print_board(board):
    print(np.flip(board, 0)) # flip the board to make it look like a real connect four game        
 
 
def winning_move(board, piece):
    # checking for horizontal win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True
     
    # checking for vertical win 
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True
 
    # checking for diagonal win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True
    
    # checking for diagonal win (negative one i.e. from upside, coming downwards)
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True
            

def draw_board_pygame(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
           
            #  empty circles
            pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), SQUARE_RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
        # player one (red circle)
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE  + SQUARE_SIZE / 2)), SQUARE_RADIUS)

        # player two (red circle)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE  + SQUARE_SIZE / 2)), SQUARE_RADIUS)
                
    pygame.display.update()    
# GAME VARIABLES 
game_over = False
board = create_board()
turn  = 0

# pygame initialization 
pygame.init()

# window / screen dimension variables

SQUARE_SIZE = 100
SQUARE_RADIUS = int(SQUARE_SIZE / 2 - 5)

width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE

size  = (width, height)

screen = pygame.display.set_mode(size)
draw_board_pygame(board)
pygame.display.update()


# GAME LOOP
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()       

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE)) # to clear the previous circle
            pos_x = event.pos[0] # the x coordinate in the position tuple
            if turn == 0:
                pygame.draw.circle(screen, RED, (pos_x, int(SQUARE_SIZE / 2)), SQUARE_RADIUS)
            else: 
                pygame.draw.circle(screen, YELLOW, (pos_x, int(SQUARE_SIZE / 2)), SQUARE_RADIUS)
        pygame.display.update()        
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if turn == 0:
                position_x = event.pos[0] # the x coordinate in the position tuple
                p_1_col_selection = int(math.floor((position_x / SQUARE_SIZE))) # the column number selected by player 1)
                if is_valid_location(board, p_1_col_selection):
                    row = get_next_open_row(board, p_1_col_selection)
                    drop_piece(board, row, p_1_col_selection, 1)
                    # print_board(board) #will print board on the cli 
                    
                    draw_board_pygame(board)
                    
                    # checking for win
                    if winning_move(board, 1):
                        print("Player 1 wins!")
                        break                    
            else:
                position_x = event.pos[0]
                p_2_col_selection = int(math.floor((position_x / SQUARE_SIZE)))
                if is_valid_location(board, p_2_col_selection):
                    row = get_next_open_row(board, p_2_col_selection)
                    drop_piece(board, row, p_2_col_selection, 2)
                    # print_board(board) #will print board on the cli
                    
                    draw_board_pygame(board)
                    
                    # checking for win
                    if winning_move(board, 2):
                        print("Player 1 wins!")
                        break
            
            turn += 1
            turn = turn % 2  # Switch turns between players            

            if game_over:
                pygame.time.wait(3000)