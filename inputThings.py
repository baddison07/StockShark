import chess
import chess.pgn
import io
import csv

def generate_move_tokens(game):
    board = game.board()
    move_tokens = []
    board_state_tokens = []
    outp = []
    for move_number, move in enumerate(game.mainline_moves(), start=1):
        if move_number == 0.01:
            move_tokens = []
        if move_number <= 100:
            # Apply the move to the board
            piece = board.piece_at(move.from_square)
            piece_type = piece.symbol().upper()
            from_square = chess.square_name(move.from_square)
            to_square = chess.square_name(move.to_square)
            color = 1 if board.turn == chess.WHITE else -1

            # Create a token for this move
            token = [
                round(move_number * 0.01, 2),
                color,
                piece_values.get(piece_type, 'Unknown'),
                position_to_value(from_square),
                position_to_value(to_square),
                0, 0, 0
            ]
            move_tokens.append(token)

            # Update the board with the move
            board.push(move)

            # Create 64 board state tokens after each move
            board_state_tokens.extend(generate_board_state_tokens(board))

            board_tokens = generate_board_state_tokens(board)
            outp.append(board_tokens + move_tokens)
    return outp

            


def generate_board_state_tokens(board):
    board_state_tokens = []

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        piece_type = piece_values.get(piece.symbol().upper(), 5) if piece else 5  # Default to 5 if no piece
        color = 1 if piece and piece.color == chess.WHITE else 0 if piece and piece.color == chess.BLACK else 5  # Default to 5 if no piece
        square_name = position_to_value(chess.square_name(square))

        # Create a board state token
        board_state_token = [0, 0, 0, 0, 0, square_name, piece_type, color]
        board_state_tokens.append(board_state_token)
    # print(board_state_tokens)
    return board_state_tokens

def process_pgn_file(file_path):

    with open(file_path, "r") as pgn_file:
        pgn = io.StringIO(pgn_file.read())
        games = [[] for i in range(100)]
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break
            gameLength = get_game_length(game)
            if gameLength >= 100:
                gameLength = 99
            games[gameLength].append(generate_move_tokens(game))
        for i in range(0, 100):
            for w in range(len(games[i])):
                csv_writer.writerow(games[i][w])
            csv_writer.writerow('|')
                
        

def get_game_length(game):
    # Counting all moves in the mainline
    num_moves = sum(1 for _ in game.mainline_moves())
    return num_moves

def position_to_value(position):
    # Mapping from file (a-h) and rank (1-8) to coordinates
    file = position[0].lower()
    rank = int(position[1])
    
    # Map file a-h to 0-7 and rank 1-8 to 0-7
    file_index = ord(file) - ord('a')
    rank_index = rank - 1
    
    # Calculate the position as a single value
    position_index = rank_index * 8 + file_index
    
    # Define the total number of squares on the board
    total_squares = 64
    
    # Value increase per square
    increment_per_square = 0.03125
    
    # Calculate the value based on the position
    value = -1 + position_index * increment_per_square
    
    return value

piece_values = {
    'P': -1,
    'N': -0.67,
    'B': -0.33,
    'R': 0.33,
    'Q': 0.67,
    'K': 1,
}

file_paths = [
    'games/Dragon_by_Komodo_3_3_64-bit_8CPU.bare.[3033].pgn', 
    'games/Dragon_by_Komodo_3_3_64-bit.bare.[3550].pgn', 
    'games/Dragon_by_Komodo_3_3_MCTS_64-bit_8CPU.bare.[1489].pgn', 
    'games/Dragon_by_Komodo_3_3_TM128_64-bit_8CPU.bare.[1197].pgn', 
    'games/Dragon_by_Komodo_3_64-bit_8CPU.bare.[1156].pgn', 
    'games/Dragon_by_Komodo_3_64-bit.bare.[2894].pgn', 
    'games/Stockfish_15_1_64-bit_8CPU.bare.[1663].pgn', 
    'games/Stockfish_15_1_64-bit.bare.[6704].pgn', 
    'games/Stockfish_15_64-bit_8CPU.bare.[2687].pgn', 
    'games/Stockfish_15_64-bit.bare.[2569].pgn', 
    'games/Stockfish_16_1_64-bit_8CPU.bare.[2982].pgn', 
    'games/Stockfish_16_1_64-bit.bare.[1994].pgn', 
    'games/Stockfish_16_64-bit_8CPU.bare.[3576].pgn', 
    'games/Stockfish_16_64-bit.bare.[2507].pgn'
]

csv_file_path = 'input_tokens.csv'  # Path to the CSV file

with open(csv_file_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write header if needed
    # csv_writer.writerow(['Move Number', 'Color', 'Piece Type', 'From Square', 'To Square', '0', '0', '0'])
    
    for path in file_paths:
        process_pgn_file(path)

print('done')