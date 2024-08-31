import chess
import chess.pgn
import io
import csv

def generate_move_tokens(game):
    board = game.board()
    move_tokens = []
    outp = []
    
    for move_number, move in enumerate(game.mainline_moves(), start=1):
        # Check if it's Stockfish's turn to move
        if board.turn == chess.WHITE:  # Assuming Stockfish is White
            # Generate a 64-length array for the move
            move_array = [0] * 64
            to_square = move.to_square
            move_array[to_square] = 1
            
            move_tokens.append(move_array)
        
        # Update the board with the move
        board.push(move)

    if move_tokens:
        outp.append(move_tokens)
        
    return outp

def process_pgn_file(file_path, csv_writer):
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
            
            move_tokens = generate_move_tokens(game)
            if move_tokens:
                games[gameLength].append(move_tokens)
        
        # Write the games to the CSV file
        for i in range(100):
            if not games[i]:
                csv_writer.writerow(['|'])
            else:
                for game in games[i]:
                    csv_writer.writerow(game)

def get_game_length(game):
    # Counting all moves in the mainline
    num_moves = sum(1 for _ in game.mainline_moves())
    return num_moves

# List of PGN file paths
file_paths = [
    # 'games/Dragon_by_Komodo_3_3_64-bit_8CPU.bare.[3033].pgn', 
    # 'games/Dragon_by_Komodo_3_3_64-bit.bare.[3550].pgn', 
    # 'games/Dragon_by_Komodo_3_3_MCTS_64-bit_8CPU.bare.[1489].pgn', 
    # 'games/Dragon_by_Komodo_3_3_TM128_64-bit_8CPU.bare.[1197].pgn', 
    'games/Dragon_by_Komodo_3_64-bit_8CPU.bare.[1156].pgn', 
    # 'games/Dragon_by_Komodo_3_64-bit.bare.[2894].pgn', 
    # 'games/Stockfish_15_1_64-bit_8CPU.bare.[1663].pgn', 
    # 'games/Stockfish_15_1_64-bit.bare.[6704].pgn', 
    # 'games/Stockfish_15_64-bit_8CPU.bare.[2687].pgn', 
    # 'games/Stockfish_15_64-bit.bare.[2569].pgn', 
    # 'games/Stockfish_16_1_64-bit_8CPU.bare.[2982].pgn', 
    # 'games/Stockfish_16_1_64-bit.bare.[1994].pgn', 
    # 'games/Stockfish_16_64-bit_8CPU.bare.[3576].pgn', 
    # 'games/Stockfish_16_64-bit.bare.[2507].pgn'
]

# Output CSV file path
csv_file_path = 'output_tokens.csv'

with open(csv_file_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Process each PGN file and write to CSV
    for path in file_paths:
        process_pgn_file(path, csv_writer)

print('done')
