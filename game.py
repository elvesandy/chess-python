import pygame.event
import pygame.display
import pygame.draw
import pygame
import copy
pygame.init()

class Piece:
    #all chess pieces will be of this class
    def __init__(self, colour, type, image):
        self.colour = colour
        self.type = type
        self.image = image
        self.enpassant = False #-1 for left, +1 for right
        self.castle = False #set to false after moving or castling
        self.attackable = False

#Create all pieces and board for game logic
bp = Piece('b', 'p', './b_pawn.png')
wp = Piece('w', 'p', './w_pawn.png')
bk = Piece('b', 'k', './b_king.png')
wk = Piece('w', 'k', './w_king.png')
br = Piece('b', 'r', './b_rook.png')
wr = Piece('w', 'r', './w_rook.png')
bb = Piece('b', 'b', './b_bishop.png')
wb = Piece('w', 'b', './w_bishop.png')
bq = Piece('b', 'q', './b_queen.png')
wq = Piece('w', 'q', './w_queen.png')
bkn = Piece('b', 'kn', './b_knight.png')
wkn = Piece('w', 'kn', './w_knight.png')

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
    piece_locations['bk'] = (0, 4)
    piece_locations['wk'] = (7, 4)
    return board

def is_valid(game_board, selected_piece, target, current_colour, king_locations):
    '''
    input: tuple (class Piece, int, int), tuple (int, int), char; 
    returns: bool

    Checks if a move is valid and returns True if it is
    target is in i-j coordinates
    use move pattern to determine possible squares
    account for piece capture, check, checkmate, castling, promoting, en passant
    '''
    ## avoids crash on empty space click
    if not target: 
        return False
    s_piece, s_i, s_j = selected_piece
    t_i, t_j = target
    t_piece = game_board[t_i][t_j]
    if s_piece.colour != current_colour: 
        return False
    #check if king is in check.  
    # current_king = king_locations[current_colour + 'k']
    # print('king_location = ', current_king)
    # check = check_check(game_board, current_king)
    #cannot capture king
    if t_piece:
        if t_piece.type == 'k':
            return False
    possible_moves = get_moves(game_board, s_piece, s_i, s_j)
    print(possible_moves)
    if target in possible_moves:
        next_move_in_check = simulate_move(game_board, selected_piece, target, current_colour, king_locations)
        print("next_move_in_check?: ", next_move_in_check)
        return not next_move_in_check
    return False
    

def simulate_move(board, selected_piece, target, current_colour, king_locations):
    '''
    checks whether moving a piece to a location will put the same colour king into check
    returns TRUE if king is still in check after moving
            FALSE if king no longer in check
    '''
    board_copy = copy.deepcopy(board)
    king_locations_copy = copy.deepcopy(king_locations)
    select_copy = copy.deepcopy(selected_piece)
    target_copy = copy.deepcopy(target)
    move_piece(board_copy, select_copy, target_copy, king_locations_copy)  
    update_check(board_copy, king_locations_copy)
    current_king_location = king_locations_copy[current_colour + 'k']
    return check_check(board_copy, current_king_location)

def get_moves(board, s_piece, s_i, s_j):
    possible_moves = []
    if s_piece.type == 'p':
        possible_moves = pawn_move(board, s_piece, s_i, s_j)
    elif s_piece.type == 'b':
        possible_moves = bishop_move(board,s_piece, s_i, s_j)
    elif s_piece.type == 'r':
        possible_moves = rook_move(board,s_piece, s_i, s_j)
    elif s_piece.type == 'kn':
        possible_moves = knight_move(board,s_piece, s_i, s_j)
    elif s_piece.type == 'q':
        possible_moves = queen_move(board,s_piece, s_i, s_j)
    elif s_piece.type == 'k':
        possible_moves = king_move(board,s_piece, s_i, s_j)
    return possible_moves

def update_check(board, king_locations):
    black_attacking = []
    white_attacking = []
    black_king = board[king_locations['bk'][0]][king_locations['bk'][1]]
    white_king = board[king_locations['wk'][0]][king_locations['wk'][1]]
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece:
                if piece.colour == 'w':
                    white_attacking.extend(get_moves(board, piece, i, j))
                else:
                    black_attacking.extend(get_moves(board, piece, i, j))
    if king_locations['bk'] in white_attacking:
        black_king.attackable = True
    else:
        black_king.attackable = False
    if king_locations['wk'] in black_attacking:
        white_king.attackable = True
    else:
        white_king.attackable = False
    return

def check_check(board, king_location):
    #check whether king is in check
    king = board[king_location[0]][king_location[1]]
    print('checking: ', king_location)

    return king.attackable

def check_checkmate(board, king_locations, current_colour):
    current_king_location = king_locations[current_colour + 'k']
    #checks if the player is first in check
    if not check_check(board, current_king_location): return False

    #loop through all of players pieces
    for i in range(8):
        for j in range(8):
            piece_to_check = board[i][j]
            if piece_to_check:
                if piece_to_check.colour == current_colour:
                    possible_moves = get_moves(board, piece_to_check, i, j)
                    #check if there exists a move player can make so king is NOT in check
                    selected_piece = (piece_to_check, i, j)
                    for target in possible_moves:
                        if not simulate_move(board, selected_piece, target, current_colour, king_locations):
                            return False
    return True
    

def move_piece(board, selected_piece, target, king_locations):
    s_piece, s_i, s_j = selected_piece
    t_i, t_j = target
    t_piece = board[t_i][t_j]
    move = True
    #pawn. en passant and promotion
    if s_piece.type == 'p':
        #en passant (initate take on valid pieces)
        if s_piece.enpassant:
            if (t_j - s_j) == s_piece.enpassant:
                if s_piece.colour == 'b': board[4][t_j] = None
                elif s_piece.colour == 'w': board[3][t_j] = None
        #en passant (set for future pieces)
        #-1 for left, +1 for right
        if s_piece.colour == 'b' and s_i == 1 and t_i == 3:
            if t_j > 0:
                enemy = board[3][t_j-1]
                if enemy:
                    if enemy.colour == 'w' and enemy.type == 'p':
                        enemy.enpassant = +1  
            if t_j < 7:
                enemy = board[3][t_j+1]
                if enemy:
                    if enemy.colour == 'w' and enemy.type == 'p':
                        enemy.enpassant = -1
        if s_piece.colour == 'w' and s_i == 6 and t_i == 4:
            if t_j > 0:
                enemy = board[4][t_j-1]
                if enemy:
                    if enemy.colour == 'b' and enemy.type == 'p':
                        enemy.enpassant = +1
            if t_j < 7:
                enemy = board[4][t_j+1]
                if enemy:
                    if enemy.colour == 'b' and enemy.type == 'p':
                        enemy.enpassant = -1   
        #promoting
        if (s_piece.colour == 'b' and t_i== 7):
            board[s_i][s_j] = None
            board[t_i][t_j] = Piece('b', 'q', './b_queen.png')
            move = False
        elif (s_piece.colour == 'w' and t_i == 0):
            board[s_i][s_j] = None
            board[t_i][t_j]  = Piece('w', 'q', './w_queen.png')
            move = False
    ##castling
    elif s_piece.type == 'k':
            if s_piece.castle: 
                #kingside castle king into rook
                if (t_i, t_j) == (7,6): 
                    board[t_i][t_j] = s_piece
                    board[7][5] = board [7][7]
                    board[7][7] = None
                    board[7][5].castle = False
                elif (t_i, t_j) == (0,6): 
                    board[t_i][t_j] = s_piece
                    board[0][5] = board [0][7]
                    board[0][7] = None
                    board[0][5].castle = False
                #queenside castle king into rook
                elif (t_i, t_j) == (7,2): 
                    board[t_i][t_j] = s_piece
                    board[7][3] = board [7][0]
                    board[7][0] = None
                    board[7][3].castle = False
                elif (t_i, t_j) == (0,2): 
                    board[t_i][t_j] = s_piece
                    board[0][3] = board [0][0]
                    board[0][0] = None
                    board[0][3].castle = False
    s_piece.castle = False
    if move:
        board[t_i][t_j] = s_piece
        board[s_i][s_j] = None
        if s_piece.type == 'k':
            king_locations[s_piece.colour + 'k'] = (t_i, t_j)
    return 


def pawn_move(board, piece, i, j):
    moves = []
    if i < 7 and i > 0:
        if piece.colour == 'b':
            #move forward if space empty
            infront = board[i+1][j]
            if infront is None:
                if i == 1: moves.append((3, j))
                moves.append((i+1, j))
            if piece.enpassant:
                moves.append((i+1, j+piece.enpassant))
            #taking pieces diagonally 
            if j > 0:
                rightside = board[i+1][j-1]
                if rightside:
                    if rightside.colour == 'w':
                        moves.append((i+1,j-1))
            if j < 7:
                leftside = board[i+1][j+1]
                if leftside:
                    if leftside.colour == 'w':
                        moves.append((i+1,j+1))
        elif piece.colour == 'w':
            #move forward if space empty
            infront = board[i-1][j]
            if infront is None:
                if i == 6: moves.append((4, j))
                moves.append((i-1, j))
            if piece.enpassant:
                moves.append((i-1, j+piece.enpassant))    
            #taking pieces diagonally 
            if j < 7:
                rightside = board[i-1][j+1]
                if rightside:
                    if rightside.colour == 'b':
                        moves.append((i-1,j+1))
            if j > 0:
                leftside = board[i-1][j-1]
                if leftside:
                    if leftside.colour == 'b':
                        moves.append((i-1,j-1))
    return moves

def bishop_move(board, piece, i, j):
    moves = []
    # visual of directions
    #   3       4
    #       b
    #   2       1
    #direction 1
    for k in range(1, 8):
        if 0 <= i+k < 8 and 0 <= j+k < 8:
            target = board[i+k][j+k]
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
            target = board[i+k][j-k]
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
            target = board[i-k][j-k]
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
            target = board[i-k][j+k]
            if not target:
                moves.append((i-k,j+k)) 
            elif target.colour != piece.colour:
                moves.append((i-k,j+k))
                break
            elif target.colour == piece.colour :
                break    
    return moves

def rook_move(board, piece, i, j):
    moves = []
    #direction 1 (down)
    for k in range(1, 8):
        if 0 <= i+k < 8:
            target = board[i+k][j]
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
            target = board[i-k][j]
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
            target = board[i][j+k]
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
            target = board[i][j-k]
            if not target:
                moves.append((i,j-k)) 
            elif target.colour != piece.colour:
                moves.append((i,j-k))
                break
            elif target.colour == piece.colour :
                break    
    return moves

def knight_move(board, piece, i, j):
    moves = []
    possible = [(i+2, j+1), (i+2, j-1), (i-2, j+1), (i-2, j-1), (i+1, j+2), (i-1, j+2), (i+1, j-2), (i-1, j-2)]
    for k in  possible:
        if 0<=k[0]<=7 and 0<=k[1]<=7:
            target = board[k[0]][k[1]]
            if not target:
                moves.append(k)
            elif target.colour != piece.colour:
                moves.append(k)
    return moves

def queen_move(board, piece, i, j):
    moves = []
    moves.extend(rook_move(board, piece, i, j))
    moves.extend(bishop_move(board, piece, i, j))
    return moves
    
def king_move(board, piece, i, j):
    moves = []
    possible = [(i+k, j+l) for k in range(-1,2) for l in range(-1,2)]
    possible.remove((i,j))
    for k in possible:
        if 0<=k[0]<=7 and 0<=k[1]<=7:
            target = board[k[0]][k[1]]
            if not target:
                moves.append(k)
            elif target.colour != piece.colour:
                moves.append(k)
    if piece.castle == True: 
        if piece.colour == 'w':
            if not game_board[7][2] and not game_board[7][3]:
                moves.append((7,2))  
            if not game_board[7][6] and not game_board[7][5]:
                moves.append((7,6))  
        if piece.colour == 'b':
            if not game_board[0][2] and not game_board[0][3]:
                moves.append((0,2))  
            if not game_board[0][6] and not game_board[0][5]:
                moves.append((0,6))  
    return moves


class Square: 
    #each grid square on chess board is of this class. 
    #height = self.width 
    def __init__(self, row, col, width, colour, piece, game_board):
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

def make_display_board(rows, cols, board_width, game_board):
    display_board = [[]for i in range(rows)]
    square_width = board_width//rows ##could use floor division //
    for i in range(rows): #i is rows, j is columns
        for j in range(cols):
            colour = CREAM
            if (i+j)%2 == 1:
                colour = BROWN
            node = Square(i, j, square_width, colour, game_board[i][j], game_board)
            display_board[i].append(node)
    return(display_board)

def update_display(screen, display_board, rows, width):
    for row in display_board:
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
TILESIZE = WIDTH//8

def get_square_under_mouse(display_board, game_board): 
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    j, i = [int(v // (WIDTH//8)) for v in mouse_pos]
    try: 
        if i >= 0 and j >= 0: return (game_board[i][j], i, j)
    except IndexError: pass
    return None, None, None

def draw_drag(screen, display_board, selected_piece):
    '''
    copied online. doesnt exactly work LOL
    investigate the screen.blit function and how to get accurate drag and drop
    '''
    if selected_piece:
        piece, i, j = get_square_under_mouse(display_board, game_board)
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

def message_display(screen, line):
    myfont = pygame.font.SysFont("franklingothicmedium", 128)
    textsurface = myfont.render(line, False, CRIMSON, CREAM)
    textRectangle = textsurface.get_rect(center = (WIDTH//2, HEIGHT//2)) 
    screen.blit(textsurface, textRectangle)
    pygame.display.update()

#initialize game board in starting position (in main)
game_board = []
piece_locations = {}

def main(screen):
    global game_board
    game_board = create_game_board()
    display_board = make_display_board(8, 8, WIDTH, game_board)
    clock = pygame.time.Clock()
    selected_piece = None
    drop_pos = None
    players = ['w', 'b'] 
    current_player = 0
    line = ''
    while True:
        piece, i, j = get_square_under_mouse(display_board, game_board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if piece != None:
                    selected_piece = piece, i, j
                    c, a, b = selected_piece
                    display_board[a][b].hide()
            if event.type == pygame.MOUSEBUTTONUP:
                check_valid = is_valid(game_board, selected_piece, drop_pos , players[current_player], piece_locations)
                print("valid move: ", check_valid)
                if check_valid == True:
                    move_piece(game_board, selected_piece, drop_pos, piece_locations)
                    update_check(game_board, piece_locations)
                    current_player = (current_player + 1) % 2
                    if check_checkmate(game_board, piece_locations, players[current_player]):
                        winner = (current_player + 1) % 2
                        if winner == 'b':
                            line = "BLACK WINS"
                        else: 
                            line = "WHITE WINS"
                        print(line)
                if selected_piece: display_board[a][b].unhide()
                selected_piece = None
                drop_pos = None
            update_display(screen, display_board, 8, WIDTH)
            drop_pos = draw_drag(screen, display_board, selected_piece)
            message_display(screen, line)
            pygame.display.flip()
            clock.tick(60)

if __name__ == '__main__':
    main(screen)