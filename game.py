import pygame.event
import pygame.display
import pygame.draw
import pygame
pygame.init()

class Piece:
    #all chess pieces will be of this class
    def __init__(self, colour, type, image):
        self.colour = colour
        self.type = type
        self.image = image
        self.enpassant = False #-1 for left, +1 for right
        self.castle = False #set to false after moving or castling
        self.check = False

#Create all pieces and board for game logic
bp = Piece('b', 'p', 'b_pawn.png')
wp = Piece('w', 'p', 'w_pawn.png')
bk = Piece('b', 'k', 'b_king.png')
wk = Piece('w', 'k', 'w_king.png')
br = Piece('b', 'r', 'b_rook.png')
wr = Piece('w', 'r', 'w_rook.png')
bb = Piece('b', 'b', 'b_bishop.png')
wb = Piece('w', 'b', 'w_bishop.png')
bq = Piece('b', 'q', 'b_queen.png')
wq = Piece('w', 'q', 'w_queen.png')
bkn = Piece('b', 'kn', 'b_knight.png')
wkn = Piece('w', 'kn', 'w_knight.png')

def create_game_board(): #return a newly set game board
    board = [[None for j in range(8)] for i in range(8)] #define an 8x8 array of values 0
    for j in range(8): 
        board[1][j] = Piece('b', 'p', 'b_pawn.png')
    board[0][0] = br
    board[0][7] = br
    board[0][1] = bkn
    board[0][6] = bkn
    board[0][2] = bb
    board[0][5] = bb     
    board[0][3] = bq
    board[0][4] = bk
    for j in range(8): 
        board[6][j] = Piece('w', 'p', 'w_pawn.png')
    board[7][0] = wr
    board[7][7] = wr
    board[7][1] = wkn
    board[7][6] = wkn
    board[7][2] = wb
    board[7][5] = wb   
    board[7][3] = wq
    board[7][4] = wk
    #rest of the pieces
    board[0][0].castle = True
    board[0][7].castle = True
    board[0][4].castle = True
    board[7][0].castle = True
    board[7][7].castle = True
    board[7][4].castle = True
    return board



def is_valid(selected_piece, target, current_colour):
    '''
    input: tuple (class Piece, int, int), (int, int); target is in i-j coordinates
    returns: bool
    Checks if a move is valid and returns True if it is
    '''
    ## doesn't run if no piece is selected
    ## avoids crash on empty space click
    if not target: 
        return False
    s_piece, s_i, s_j = selected_piece
    t_i, t_j = target
    t_piece = game_board[t_i][t_j]
    if s_piece.colour != current_colour: 
        return

    check = check_check(current_colour)
    if check:
        if s_piece.type != 'k':
            return False

    possible_moves = []
    if s_piece.type == 'p':
        possible_moves = pawn_move(s_piece, s_i, s_j)
    elif s_piece.type == 'b':
        possible_moves = bishop_move(s_piece, s_i, s_j)
    elif s_piece.type == 'r':
        possible_moves = rook_move(s_piece, s_i, s_j)
    elif s_piece.type == 'kn':
        possible_moves = knight_move(s_piece, s_i, s_j)
    elif s_piece.type == 'q':
        possible_moves = queen_move(s_piece, s_i, s_j)
    elif s_piece.type == 'k':
        possible_moves = king_move(s_piece, s_i, s_j)
    
    if t_piece:
        if t_piece.type == 'k':
            return
    ##use move pattern to determine possible squares
    ##account for piece capture, check, checkmate, castling, promoting, en passant

    #castle condition
    ## 1. must be king and rooks first move
    ## 2. king cannot move through check / into check
    ## 3. king cannot castle while under attack
    
    if s_piece == 'k' and not check:
        #get square
        print("do stuff")
    print(possible_moves)
    if target in possible_moves:
        return True
    return False

def check_check(current_colour):
    #check whether king is in check
    answer = True
    return False

def move_piece(selected_piece, target):
    s_piece, s_i, s_j = selected_piece
    t_i, t_j = target
    t_piece = game_board[t_i][t_j]
    move = True
    #pawn. en passant and promotion
    if s_piece.type == 'p':
        #en passant (initate take on valid pieces)
        if s_piece.enpassant:
            if (t_j - s_j) == s_piece.enpassant:
                if s_piece.colour == 'b': game_board[4][t_j] = None
                elif s_piece.colour == 'w': game_board[3][t_j] = None
        #en passant (set for future pieces)
        #-1 for left, +1 for right
        if s_piece.colour == 'b' and s_i == 1 and t_i == 3:
            if t_j > 0:
                enemy = game_board[3][t_j-1]
                if enemy:
                    if enemy.colour == 'w' and enemy.type == 'p':
                        enemy.enpassant = +1  
            if t_j < 7:
                enemy = game_board[3][t_j+1]
                if enemy:
                    if enemy.colour == 'w' and enemy.type == 'p':
                        enemy.enpassant = -1
        if s_piece.colour == 'w' and s_i == 6 and t_i == 4:
            if t_j > 0:
                enemy = game_board[4][t_j-1]
                if enemy:
                    if enemy.colour == 'b' and enemy.type == 'p':
                        enemy.enpassant = +1
            if t_j < 7:
                enemy = game_board[4][t_j+1]
                if enemy:
                    if enemy.colour == 'b' and enemy.type == 'p':
                        enemy.enpassant = -1   
    ##castling
    elif s_piece.type == 'k':
            if s_piece.castle: 
                #kingside castle king into rook
                if (t_i, t_j) == (7,6): 
                    game_board[t_i][t_j] = s_piece
                    game_board[7][5] = game_board [7][7]
                    game_board[7][7] = None
                    game_board[7][5].castle = False
                elif (t_i, t_j) == (0,6): 
                    game_board[t_i][t_j] = s_piece
                    game_board[0][5] = game_board [0][7]
                    game_board[0][7] = None
                    game_board[0][5].castle = False
                #queenside castle king into rook
                elif (t_i, t_j) == (7,2): 
                    game_board[t_i][t_j] = s_piece
                    game_board[7][3] = game_board [7][0]
                    game_board[7][0] = None
                    game_board[7][3].castle = False
                elif (t_i, t_j) == (0,2): 
                    game_board[t_i][t_j] = s_piece
                    game_board[0][3] = game_board [0][0]
                    game_board[0][0] = None
                    game_board[0][3].castle = False
    s_piece.castle = False
    if move:
        game_board[t_i][t_j] = s_piece
        game_board[s_i][s_j] = None
    return 


def pawn_move(piece, i, j):
    moves = []
    if i < 7 and i > 0:
        if piece.colour == 'b':
            infront = game_board[i+1][j]
            if infront is None:
                if i == 1: moves.append((3, j))
                moves.append((i+1, j))
            if piece.enpassant:
                moves.append((i+1, j+piece.enpassant))
            ##taking pieces diagonally 
            if j > 0 and j < 7:
                leftside = game_board[i+1][j+1]
                rightside = game_board[i+1][j-1]
                if leftside:
                    if leftside.colour == 'w' and leftside.type != 'k':
                        moves.append((i+1,j+1))
                if rightside:
                    if rightside.colour == 'w' and rightside.type != 'k':
                        moves.append((i+1,j-1))
        elif piece.colour == 'w':
            infront = game_board[i-1][j]
            if infront is None:
                if i == 6: moves.append((4, j))
                moves.append((i-1, j))
            if piece.enpassant:
                moves.append((i-1, j+piece.enpassant))                
            if j > 0 and j < 7:
                leftside = game_board[i-1][j-1]
                rightside = game_board[i-1][j+1]
                if leftside:
                    if leftside.colour == 'b' and leftside.type != 'k':
                        moves.append((i-1,j-1))
                if rightside:
                    if rightside.colour == 'b' and rightside.type != 'k':
                        moves.append((i-1,j+1))
    return moves

def bishop_move(piece, i, j):
    moves = []
    # visual of directions
    #   3       4
    #       b
    #   2       1
    #direction 1
    for k in range(1, 8):
        if 0 <= i+k < 8 and 0 <= j+k < 8:
            target = game_board[i+k][j+k]
            if not target:
                moves.append((i+k,j+k)) 
            elif target.colour != piece.colour:
                moves.append((i+k,j+k))
                break
            elif target.colour == piece.colour:
                break
    #direction 2
    for k in range(1, 8):
        if 0 <= i+k < 8 and 0 <= j-k < 8:
            target = game_board[i+k][j-k]
            if not target:
                moves.append((i+k,j-k)) 
            elif target.colour != piece.colour:
                moves.append((i+k,j-k))
                break
            elif target.colour == piece.colour :
                break
    #direction 3
    for k in range(1, 8):
        if 0 <= i-k < 8 and 0 <= j-k < 8:
            target = game_board[i-k][j-k]
            if not target:
                moves.append((i-k,j-k)) 
            elif target.colour != piece.colour:
                moves.append((i-k,j-k))
                break
            elif target.colour == piece.colour :
                break    
    #direction 4
    for k in range(1, 8):
        if 0 <= i-k < 8 and 0 <= j+k < 8:
            target = game_board[i-k][j+k]
            if not target:
                moves.append((i-k,j+k)) 
            elif target.colour != piece.colour:
                moves.append((i-k,j+k))
                break
            elif target.colour == piece.colour :
                break    
    return moves

def rook_move(piece, i, j):
    moves = []
    #direction 1 (down)
    for k in range(1, 8):
        if 0 <= i+k < 8:
            target = game_board[i+k][j]
            if not target:
                moves.append((i+k,j)) 
            elif target.colour != piece.colour:
                moves.append((i+k,j))
                break
            elif target.colour == piece.colour:
                break
    # #direction 2 (up)
    for k in range(1, 8):
        if 0 <= i-k < 8:
            target = game_board[i-k][j]
            if not target:
                moves.append((i-k,j)) 
            elif target.colour != piece.colour:
                moves.append((i-k,j))
                break
            elif target.colour == piece.colour :
                break    
    # #direction 3 (right)
    for k in range(1, 8):
        if 0 <= j+k < 8:
            target = game_board[i][j+k]
            if not target:
                moves.append((i,j+k)) 
            elif target.colour != piece.colour:
                moves.append((i,j+k))
                break
            elif target.colour == piece.colour :
                break   
    # #direction 4 (left)
    for k in range(1, 8):
        if 0 <= j-k < 8:
            target = game_board[i][j-k]
            if not target:
                moves.append((i,j-k)) 
            elif target.colour != piece.colour:
                moves.append((i,j-k))
                break
            elif target.colour == piece.colour :
                break    
    
    return moves

def knight_move(piece, i, j):
    moves = []
    possible = [(i+2, j+1), (i+2, j-1), (i-2, j+1), (i-2, j-1), (i+1, j+2), (i-1, j+2), (i+1, j-2), (i-1, j-2)]
    for k in  possible:
        if 0<=k[0]<=7 and 0<=k[1]<=7:
            target = game_board[k[0]][k[1]]
            if not target:
                moves.append(k)
            elif target.colour != piece.colour:
                moves.append(k)
    return moves

def queen_move(piece, i, j):
    moves = []
    moves.extend(rook_move(piece, i, j))
    moves.extend(bishop_move(piece, i, j))
    return moves
    
def king_move(piece, i, j):
    moves = []
    possible = [(i+k, j+l) for k in range(-1,2) for l in range(-1,2)]
    possible.remove((i,j))
    for k in possible:
        if 0<=k[0]<=7 and 0<=k[1]<=7:
            target = game_board[k[0]][k[1]]
            if not target:
                moves.append(k)
            elif target.colour != piece.colour:
                moves.append(k)
    if piece.castle == True: 
        if piece.colour == 'w':
            moves.append((7,2))  
            moves.append((7,6))  
        if piece.colour == 'b':
            moves.append((0,2))  
            moves.append((0,6))  
    return moves


class Square: 
    #each grid square on chess board is of this class. 
    #height = self.width 
    def __init__(self, row, col, width, colour, piece):
        self.row = row
        self.col = col
        self.width = width
        self.colour = colour    
        self.piece = game_board[self.row][self.col]
        #bottom left coordinates of square
        self.x = int(col * width)
        self.y = int(row * width)
        self.hidden = False

    def draw_square(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.width))

    def setup(self, screen): #draw pieces
        self.piece = game_board[self.row][self.col]
        if self.piece and not self.hidden: 
            screen.blit(pygame.image.load(self.piece.image), (self.x + 18 , self.y + 20))

    def hide(self):
        self.hidden = True
        
    def unhide(self):
        self.hidden = False

#Colours to be used
BROWN = (202, 111, 57)
CREAM = (244, 225, 189)
CRIMSON = (113, 32,24)
BLACK = (0, 0, 0)

def make_board(rows, cols, board_width):
    board = [[]for i in range(rows)]
    square_width = board_width//rows ##could use floor division //
    for i in range(rows): #i is rows, j is columns
        for j in range(cols):
            colour = CREAM
            if (i+j)%2 == 1:
                colour = BROWN
            node = Square(i, j, square_width, colour, game_board[i][j])
            board[i].append(node)
    return(board)

def update_display(screen, board, rows, width):
    for row in board:
        for node in row:
            node.draw_square(screen)
            node.setup(screen)
    pygame.display.update()

#Create the screen for the game
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
BOARD_POS = (10, 10)

def get_square_under_mouse(display_board): 
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    j, i = [int(v // (WIDTH//8)) for v in mouse_pos]
    try: 
        if i >= 0 and j >= 0: return (game_board[i][j], i, j)
    except IndexError: pass
    return None, None, None

TILESIZE = WIDTH//8

def draw_drag(screen, display_board, selected_piece):
    '''
    copied online. doesnt exactly work LOL
    investigate the screen.blit function and how to get accurate drag and drop
    '''
    if selected_piece:
        piece, i, j = get_square_under_mouse(display_board)
        if i != None:
            rect = (j * TILESIZE, i * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)
        pos = pygame.Vector2(pygame.mouse.get_pos())
        screen.blit(pygame.image.load(selected_piece[0].image),pygame.image.load(selected_piece[0].image).get_rect(center=pos))
        # display_board[selected_piece[1]][selected_piece[2]].hide(screen)
        # screen.blit(pygame.image.load(selected_piece[0].image), pygame.image.load(selected_piece[0].image).get_rect(center=pos))
        selected_rect = pygame.Rect(selected_piece[2] * TILESIZE, selected_piece[1] * TILESIZE, TILESIZE, TILESIZE)
        # pygame.draw.line(screen, pygame.Color('red'), selected_rect.center, pos)
        return (i, j)

#initialize game board in starting position (in main)
game_board = []

def main(screen):
    global game_board
    game_board = create_game_board()
    display_board = make_board(8, 8, WIDTH)
    clock = pygame.time.Clock()
    selected_piece = None
    drop_pos = None
    players = ['w', 'b'] 
    current_player = 0
    while True:
        piece, i, j = get_square_under_mouse(display_board)
        # if piece:
        #     print(piece.type, i, j)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if piece != None:
                    selected_piece = piece, i, j
                    # print(i, j)
                    print(display_board[i][j].piece.type)
                    print(display_board[i][j].row, display_board[i][j].col)
                    print(game_board[i][j].castle)
                    c, a, b = selected_piece
                    display_board[a][b].hide()
            if event.type == pygame.MOUSEBUTTONUP:
                check = is_valid(selected_piece, drop_pos , players[current_player])
                if check:
                    move_piece(selected_piece, drop_pos)
                    current_player = (current_player + 1) % 2
                    #remove below lines once isValid implemented
                    # piece, old_i, old_j = selected_piece
                    # game_board[old_i][old_j] = None
                    # new_i, new_j = drop_pos
                    # game_board[new_i][new_j] = piece
                if selected_piece: display_board[a][b].unhide()
                selected_piece = None
                drop_pos = None
            update_display(screen, display_board, 8, WIDTH)
            drop_pos = draw_drag(screen, display_board, selected_piece)
            pygame.display.flip()
            clock.tick(60)
if __name__ == '__main__':
    main(screen)