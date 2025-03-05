import random
import pygame
import chess

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOARD_COLOR_1 = (235, 209, 166)
BOARD_COLOR_2 = (165, 117, 81)
HIGHLIGHT_COLOR = (255, 255, 0)

BOARD_SIZE = 480  # 480x480 pixels
SQUARE_SIZE = BOARD_SIZE // 8  # 8x8 grid

screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption('Chess Board')

board = chess.Board()

font = pygame.font.Font(r"C:\Windows\Fonts\Arial.ttf", 32)

piece_images = {}
for piece in ['r', 'n', 'b', 'q', 'k', 'p', 'R', 'N', 'B', 'Q', 'K', 'P', 'r_ROOKMEO', 'R_ROOKMEO']:
    piece_images[piece] = pygame.transform.scale(
        pygame.image.load(f'images/{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE))


def draw_board():
    for row in range(8):
        for col in range(8):
            color = BOARD_COLOR_1 if (row + col) % 2 == 0 else BOARD_COLOR_2
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(board):
    for row in range(8):
        for col in range(8):
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                screen.blit(piece_images[piece.symbol()],
                            pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def get_square_under_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return chess.square(col, 7 - row)


def highlight_moves(legal_moves):
    for move in legal_moves:
        to_square = move.to_square
        col = chess.square_file(to_square)
        row = 7 - chess.square_rank(to_square)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR,
                         pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def choose_two_rooks(board):
    white_rooks = []
    black_rooks = []

    # Loop through all squares on the board to find the rooks
    for square in chess.SQUARES:
        piece = board.piece_at(square)

        # Check if the piece is a white rook
        if piece and piece.piece_type == chess.ROOK and piece.color == chess.WHITE:
            # Make sure to append the square, otherwise every rook will be considered rookmeo.
            white_rooks.append(square)

        # Check if the piece is a black rook
        if piece and piece.piece_type == chess.ROOK and piece.color == chess.BLACK:
            # Same for this one.
            black_rooks.append(square)

    selected_white_rook = random.choice(white_rooks)
    selected_black_rook = random.choice(black_rooks)
    return selected_white_rook, selected_black_rook


def has_rook_moved(rook, board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece == rook:
            return False
    return True


def rooks_looking_at_each_other(rookmeo_square, juliet_square, board):
    if rookmeo_square is None or juliet_square is None:
        return

    # Get the row and column of each rook
    rookmeo_row = chess.square_rank(rookmeo_square)
    rookmeo_col = chess.square_file(rookmeo_square)
    juliet_row = chess.square_rank(juliet_square)
    juliet_col = chess.square_file(juliet_square)

    # Check if they are in the same row or column
    if rookmeo_row == juliet_row:  # Same row
        # Ensure there are no pieces between them along the row
        step = 1 if rookmeo_col < juliet_col else -1
        for col in range(rookmeo_col + step, juliet_col, step):
            if board.piece_at(chess.square(col, rookmeo_row)):  # Check for any piece in between
                return False
        return True

    elif rookmeo_col == juliet_col:  # Same column
        # Ensure there are no pieces between them along the column
        step = 1 if rookmeo_row < juliet_row else -1
        for row in range(rookmeo_row + step, juliet_row, step):
            if board.piece_at(chess.square(rookmeo_col, row)):  # Check for any piece in between
                return False
        return True

    return False

def select_piece(square):
    if not board.piece_at(square):
        return None
    elif board.piece_at(square).color == (chess.WHITE if board.turn else chess.BLACK):
        return square

def set_promotion(selected_square ,square):
    promotion = None
    piece = board.piece_at(selected_square)
    if piece.piece_type == chess.PAWN and piece.color == chess.WHITE and chess.square_rank(square) == 7:
        promotion = chess.QUEEN
    elif piece.piece_type == chess.PAWN and piece.color == chess.BLACK and chess.square_rank(square) == 0:
        promotion = chess.QUEEN
    return promotion

def make_move(move: chess.Move):
    if game_over:
        return
    board.push(move)
    update_special_position(move)

def update_special_position(move: chess.Move):
    global rookmeo, juliet

    if move.to_square == rookmeo:
        rookmeo = None
        board.set_piece_at(juliet, chess.Piece(chess.QUEEN, chess.WHITE))

        # deinitialize so that the game doesnt try to render a queen juliet
        juliet = None

    if move.to_square == juliet:
        juliet = None
        board.set_piece_at(rookmeo, chess.Piece(chess.QUEEN, chess.BLACK))

        # deinitialize so that the game doesnt try to render a queen rookmeo
        rookmeo = None
    
    if move.from_square == rookmeo:
        rookmeo = square  # Update rookmeo's position to the new square

    elif move.from_square == juliet:
        juliet = square  # Update juliet's position to the new square

    piece = board.piece_at(move.to_square)
    if piece and piece.piece_type == chess.KING:
        if abs(chess.square_file(move.from_square) - chess.square_file(move.to_square)) == 2:
            # Determine which side of the board was castled
            if move.to_square == chess.G1:  # White short castling
                rook_from, rook_to = chess.H1, chess.F1
            elif move.to_square == chess.C1:  # White long castling
                rook_from, rook_to = chess.A1, chess.D1
            elif move.to_square == chess.G8:  # Black short castling
                rook_from, rook_to = chess.H8, chess.F8
            elif move.to_square == chess.C8:  # Black long castling
                rook_from, rook_to = chess.A8, chess.D8
            else:
                return  # Not a castling move

            # Update rookmeo or juliet if they were the castling rook
            if rookmeo == rook_from:
                rookmeo = rook_to
            elif juliet == rook_from:
                juliet = rook_to

# Main loop
running = True
rookmeo, juliet = choose_two_rooks(board)
text = None
game_over = False
selected_square = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                continue
            
            mouse_pos = pygame.mouse.get_pos()
            square = get_square_under_mouse(mouse_pos)

            if selected_square is None:
                # Select a piece
                selected_square = select_piece(square)
            else:
                # Move the piece
                promotion = set_promotion(selected_square, square)
                move = chess.Move(from_square=selected_square, to_square=square, promotion=promotion)

                if board.is_legal(move):
                    make_move(move)
                    selected_square = None

                    # Check if the game is over
                    if board.is_game_over(claim_draw=True):
                        outcome = board.outcome(claim_draw=True)
                        if outcome.result() == "1/2-1/2":
                            result = "DRAW"
                        elif outcome.result() == "1-0":
                            result = "WHITE WINS"
                        elif outcome.result() == "0-1":
                            result = "BLACK WINS"
                        text = font.render(result, True, WHITE)

                    if rooks_looking_at_each_other(rookmeo, juliet, board):
                        game_over = True
                        if board.turn == chess.WHITE:
                            result = "BLACK WINS"
                        elif board.turn == chess.BLACK:
                            result = "WHITE WINS"
                        text = font.render(result, True, WHITE)
                else:
                    # The user might have tried to choose a different piece.
                    selected_square = select_piece(square)


    # Draw the board and pieces
    draw_board()

    if selected_square is not None:
        legal_moves = [move for move in board.legal_moves if move.from_square == selected_square]
        highlight_moves(legal_moves)

    draw_pieces(board)

    if text:
        textRect = text.get_rect()
        textRect.center = (BOARD_SIZE // 2, BOARD_SIZE // 2)
        screen.blit(text, textRect)

    # Update the display
    pygame.display.flip()

pygame.quit()
