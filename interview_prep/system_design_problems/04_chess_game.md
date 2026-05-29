# Chess Game System Design

## Requirements

### Functional
- Two players play chess
- Track board state
- Validate moves
- Detect check/checkmate
- Maintain move history
- Replay games

### Non-Functional
- Support online multiplayer
- Messages < 100ms latency
- Handle disconnections
- Persistence

## System Architecture

```
Frontend                Backend              Database
(UI Board)         (Game Logic)           (Game State)
   |                  |                       |
   |--move cmd------->|                       |
   |                  |--validate move        |
   |                  |--update board         |
   |                  |--save state---------->|
   |<--board state----|                       |
   |                  |                       |
```

## Core Classes

```python
class Piece:
    def __init__(self, color, piece_type):
        self.color = color  # WHITE, BLACK
        self.piece_type = piece_type  # PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING
    
    def get_valid_moves(self, position, board):
        # Piece-specific move logic
        pass

class Position:
    def __init__(self, row, col):
        self.row = row  # 0-7
        self.col = col  # 0-7

class BoardState:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_pieces()
    
    def initialize_pieces(self):
        # Set up initial chess position
        pass
    
    def is_valid_position(self, pos):
        return 0 <= pos.row < 8 and 0 <= pos.col < 8
    
    def get_piece(self, pos):
        return self.board[pos.row][pos.col]
    
    def set_piece(self, pos, piece):
        self.board[pos.row][pos.col] = piece
    
    def is_under_attack(self, pos, by_color):
        # Check if position attacked by color
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == by_color:
                    moves = piece.get_valid_moves(Position(row, col), self)
                    if pos in moves:
                        return True
        return False
    
    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.piece_type == "KING" and piece.color == color:
                    return Position(row, col)
        return None

class Game:
    def __init__(self, player1_id, player2_id):
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.board = BoardState()
        self.current_turn = "WHITE"
        self.move_history = []
        self.status = "IN_PROGRESS"  # IN_PROGRESS, CHECKMATE, STALEMATE, DRAW
    
    def make_move(self, from_pos, to_pos, player_id):
        # Validate player turn
        if self.get_player_color(player_id) != self.current_turn:
            return False, "Not your turn"
        
        # Get piece
        piece = self.board.get_piece(from_pos)
        if not piece:
            return False, "No piece at source"
        
        # Get valid moves
        valid_moves = piece.get_valid_moves(from_pos, self.board)
        if to_pos not in valid_moves:
            return False, "Invalid move for piece"
        
        # Simulate move and check if king in check
        self._simulate_move(from_pos, to_pos)
        
        king_pos = self.board.find_king(self.current_turn)
        if self.board.is_under_attack(king_pos, self._opponent_color()):
            self._undo_move()
            return False, "Move leaves king in check"
        
        # Make official move
        self.board.set_piece(to_pos, piece)
        self.board.set_piece(from_pos, None)
        
        # Record move
        self.move_history.append({
            "from": from_pos,
            "to": to_pos,
            "piece": piece,
            "timestamp": time.time()
        })
        
        # Check game status
        self._check_game_status()
        
        # Switch turn
        self.current_turn = self._opponent_color()
        
        return True, "Move successful"
    
    def is_in_check(self, color):
        king_pos = self.board.find_king(color)
        return self.board.is_under_attack(king_pos, self._opponent_color(color))
    
    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False
        
        # No legal moves available
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece and piece.color == color:
                    moves = piece.get_valid_moves(Position(row, col), self.board)
                    if moves:
                        return False
        
        return True
    
    def _check_game_status(self):
        if self.is_checkmate("BLACK"):
            self.status = "WHITE_WINS_CHECKMATE"
        elif self.is_checkmate("WHITE"):
            self.status = "BLACK_WINS_CHECKMATE"
        # Handle stalemate, threefold repetition, etc.
    
    def get_board_state(self):
        return [[self.board.get_piece(Position(row, col))
                 for col in range(8)]
                for row in range(8)]
    
    def get_player_color(self, player_id):
        return "WHITE" if player_id == self.player1_id else "BLACK"

class GameRepository:
    def save_game(self, game):
        # Save to database
        pass
    
    def load_game(self, game_id):
        # Load from database
        pass
    
    def get_move_history(self, game_id):
        # Return all moves
        pass
```

## Piece-Specific Logic

```python
class Pawn(Piece):
    def get_valid_moves(self, position, board):
        moves = []
        direction = -1 if self.color == "WHITE" else 1
        
        # Move forward
        forward = Position(position.row + direction, position.col)
        if board.is_valid_position(forward) and not board.get_piece(forward):
            moves.append(forward)
        
        # Capture diagonally
        for col_offset in [-1, 1]:
            capture = Position(position.row + direction, 
                             position.col + col_offset)
            if board.is_valid_position(capture):
                target = board.get_piece(capture)
                if target and target.color != self.color:
                    moves.append(capture)
        
        return moves

class Knight(Piece):
    def get_valid_moves(self, position, board):
        moves = []
        offsets = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for row_offset, col_offset in offsets:
            new_pos = Position(position.row + row_offset, 
                             position.col + col_offset)
            if board.is_valid_position(new_pos):
                target = board.get_piece(new_pos)
                if not target or target.color != self.color:
                    moves.append(new_pos)
        
        return moves

class King(Piece):
    def get_valid_moves(self, position, board):
        moves = []
        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                if row_offset == 0 and col_offset == 0:
                    continue
                
                new_pos = Position(position.row + row_offset,
                                 position.col + col_offset)
                if board.is_valid_position(new_pos):
                    target = board.get_piece(new_pos)
                    if not target or target.color != self.color:
                        moves.append(new_pos)
        
        return moves
```

## Game Flow

```
1. User1 initiates game, invites User2
2. Both players connected
3. WhitePlayer (User1) moves
4. Server validates move
5. Board updated
6. All players get new board state
7. BlackPlayer (User2) moves
8. Repeat until end
9. Save game result
```

## Key Design Decisions

| Aspect | Decision | Reason |
|--------|----------|--------|
| **Move Validation** | Server-side | Security, prevents cheating |
| **Board State** | Immutable snapshots | Easy undo/redo, history |
| **Check Detection** | Algorithm-based | Can be optimized |
| **Piece Logic** | Inheritance | Different pieces, same interface |
| **Persistence** | Move history | Can replay any game |

## Extension Ideas

1. **Time Controls**: Add clock, time management
2. **Ratings**: Elo ratings, ranked matches
3. **Analysis**: Post-game analysis, computer suggestions
4. **Tournaments**: Round-robin, bracket systems
5. **Spectators**: Watch other games
6. **Elo ratings system**
7. **Opening database**
8. **Endgame tablebases**

## Key Interview Discussion Points

1. **How to handle disconnections?**
   - Reconnect within timeout, claim win if timeout

2. **How to prevent cheating?**
   - Server validates all moves, secure authentication

3. **How to scale for millions of games?**
   - Sharding by game_id, cache active games, archive old games

4. **How to implement undo?**
   - Store move history, allow take-back in time control

5. **Draw offers?**
   - Both players agree, record in history
