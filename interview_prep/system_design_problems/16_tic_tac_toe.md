# Tic Tac Toe Game System Design

## Requirements

### Functional
- Single player (human vs AI) or multiplayer
- AI player with optimal strategy
- Game state tracking
- Win/Draw detection
- Move history/undo
- Difficulty levels
- Save/load game

### Non-Functional
- Fast AI response (< 100ms)
- Optimal play (never lose if going first with valid play)
- Extensible to larger boards (4x4, 5x5)
- Real-time multiplayer support

## Core Design: Game State

### Data Structure

```python
class TicTacToe:
    def __init__(self, board_size=3):
        self.size = board_size
        self.board = [['' for _ in range(board_size)] for _ in range(board_size)]
        self.move_history = []
        self.current_player = 'X'
    
    def make_move(self, row: int, col: int, player: str) -> bool:
        """Make move if valid"""
        if not self._is_valid_move(row, col):
            return False
        
        self.board[row][col] = player
        self.move_history.append((row, col, player))
        self.current_player = 'O' if player == 'X' else 'X'
        
        return True
    
    def _is_valid_move(self, row: int, col: int) -> bool:
        """Check bounds and empty cell"""
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return False
        
        return self.board[row][col] == ''
    
    def get_available_moves(self) -> list:
        """Get all empty cells"""
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == '':
                    moves.append((row, col))
        
        return moves
    
    def check_winner(self) -> str:
        """Check for winner - returns 'X', 'O', or ''"""
        
        # Check rows
        for row in range(self.size):
            if (all(self.board[row][col] == 'X' for col in range(self.size))):
                return 'X'
            if (all(self.board[row][col] == 'O' for col in range(self.size))):
                return 'O'
        
        # Check columns
        for col in range(self.size):
            if (all(self.board[row][col] == 'X' for row in range(self.size))):
                return 'X'
            if (all(self.board[row][col] == 'O' for row in range(self.size))):
                return 'O'
        
        # Check main diagonal
        if (all(self.board[i][i] == 'X' for i in range(self.size))):
            return 'X'
        if (all(self.board[i][i] == 'O' for i in range(self.size))):
            return 'O'
        
        # Check anti-diagonal
        if (all(self.board[i][self.size - 1 - i] == 'X' for i in range(self.size))):
            return 'X'
        if (all(self.board[i][self.size - 1 - i] == 'O' for i in range(self.size))):
            return 'O'
        
        return ''
    
    def is_draw(self) -> bool:
        """Check if board full"""
        return len(self.get_available_moves()) == 0
    
    def is_game_over(self) -> bool:
        """Check if game ended"""
        return self.check_winner() != '' or self.is_draw()
    
    def print_board(self):
        """Display board"""
        print("\n")
        for row in self.board:
            print(" | ".join(cell or " " for cell in row))
            print("---------")
```

## AI Strategy: Minimax Algorithm

### Minimax with Alpha-Beta Pruning

```python
class AIPlayer:
    def __init__(self, ai_symbol='O', difficulty='hard'):
        self.ai_symbol = ai_symbol
        self.human_symbol = 'X'
        self.difficulty = difficulty
    
    def get_best_move(self, game: TicTacToe) -> tuple:
        """Best move for AI"""
        if self.difficulty == 'easy':
            return self._get_random_move(game)
        elif self.difficulty == 'medium':
            return self._get_strategic_move(game)
        else:  # hard
            return self._get_minimax_move(game)
    
    def _get_random_move(self, game: TicTacToe) -> tuple:
        """Random valid move (easy)"""
        import random
        moves = game.get_available_moves()
        return random.choice(moves) if moves else None
    
    def _get_strategic_move(self, game: TicTacToe) -> tuple:
        """Heuristic-based move (medium)"""
        moves = game.get_available_moves()
        
        # Priority: 1. Win, 2. Block opponent, 3. Center, 4. Corner, 5. Edge
        
        # Can we win?
        for move in moves:
            game.board[move[0]][move[1]] = self.ai_symbol
            if game.check_winner() == self.ai_symbol:
                game.board[move[0]][move[1]] = ''
                return move
            game.board[move[0]][move[1]] = ''
        
        # Can we block opponent?
        for move in moves:
            game.board[move[0]][move[1]] = self.human_symbol
            if game.check_winner() == self.human_symbol:
                game.board[move[0]][move[1]] = ''
                return move
            game.board[move[0]][move[1]] = ''
        
        # Take center
        if game.size % 2 == 1:
            center = game.size // 2
            if (center, center) in moves:
                return (center, center)
        
        # Take corner
        corners = [(0, 0), (0, game.size-1), (game.size-1, 0), (game.size-1, game.size-1)]
        for corner in corners:
            if corner in moves:
                return corner
        
        # Take any valid move
        return moves[0] if moves else None
    
    def _get_minimax_move(self, game: TicTacToe) -> tuple:
        """Optimal move using minimax (hard)"""
        best_score = float('-inf')
        best_move = None
        
        for move in game.get_available_moves():
            row, col = move
            game.board[row][col] = self.ai_symbol
            
            score = self._minimax(game, 0, False, float('-inf'), float('inf'))
            
            game.board[row][col] = ''
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def _minimax(self, game: TicTacToe, depth: int, is_maximizing: bool,
                  alpha: float, beta: float) -> int:
        """Minimax with alpha-beta pruning"""
        
        # Terminal states
        winner = game.check_winner()
        if winner == self.ai_symbol:
            return 10 - depth  # Prefer faster wins
        elif winner == self.human_symbol:
            return depth - 10  # Prefer slower losses
        elif game.is_draw():
            return 0
        
        if is_maximizing:
            max_score = float('-inf')
            for move in game.get_available_moves():
                row, col = move
                game.board[row][col] = self.ai_symbol
                
                score = self._minimax(game, depth + 1, False, alpha, beta)
                
                game.board[row][col] = ''
                
                max_score = max(score, max_score)
                alpha = max(alpha, score)
                
                # Alpha-beta pruning
                if beta <= alpha:
                    break
            
            return max_score
        
        else:  # minimizing
            min_score = float('inf')
            for move in game.get_available_moves():
                row, col = move
                game.board[row][col] = self.human_symbol
                
                score = self._minimax(game, depth + 1, True, alpha, beta)
                
                game.board[row][col] = ''
                
                min_score = min(score, min_score)
                beta = min(beta, score)
                
                # Alpha-beta pruning
                if beta <= alpha:
                    break
            
            return min_score
```

### Performance Optimization: Memoization

```python
class AIPlayerOptimized:
    def __init__(self, ai_symbol='O'):
        self.ai_symbol = ai_symbol
        self.human_symbol = 'X'
        self.memo = {}  # {board_state: best_score}
    
    def _board_to_key(self, board):
        """Convert board to hashable key"""
        return tuple(tuple(row) for row in board)
    
    def _minimax_memo(self, game: TicTacToe, depth: int, 
                      is_maximizing: bool) -> int:
        """Minimax with memoization"""
        
        board_key = self._board_to_key(game.board)
        memo_key = (board_key, is_maximizing)
        
        if memo_key in self.memo:
            return self.memo[memo_key]
        
        # Terminal states
        winner = game.check_winner()
        if winner == self.ai_symbol:
            return 10 - depth
        elif winner == self.human_symbol:
            return depth - 10
        elif game.is_draw():
            return 0
        
        if is_maximizing:
            max_score = float('-inf')
            for move in game.get_available_moves():
                row, col = move
                game.board[row][col] = self.ai_symbol
                
                score = self._minimax_memo(game, depth + 1, False)
                
                game.board[row][col] = ''
                max_score = max(score, max_score)
        
        else:
            min_score = float('inf')
            for move in game.get_available_moves():
                row, col = move
                game.board[row][col] = self.human_symbol
                
                score = self._minimax_memo(game, depth + 1, True)
                
                game.board[row][col] = ''
                min_score = min(score, min_score)
        
        result = max_score if is_maximizing else min_score
        self.memo[memo_key] = result
        
        return result
```

## Game Controller

```python
class GameController:
    def __init__(self, difficulty='hard'):
        self.game = TicTacToe()
        self.ai = AIPlayer(difficulty=difficulty)
        self.game_over = False
        self.winner = ''
    
    def play_round(self, row: int, col: int):
        """Human makes move"""
        if not self.game.make_move(row, col, 'X'):
            return False, "Invalid move"
        
        # Check if human won
        if self.game.check_winner() == 'X':
            self.game_over = True
            self.winner = 'Human'
            return True, "You won!"
        
        if self.game.is_draw():
            self.game_over = True
            self.winner = 'Draw'
            return True, "Draw!"
        
        # AI makes move
        ai_move = self.ai.get_best_move(self.game)
        if ai_move:
            self.game.make_move(ai_move[0], ai_move[1], 'O')
        
        # Check if AI won
        if self.game.check_winner() == 'O':
            self.game_over = True
            self.winner = 'AI'
            return True, "AI won!"
        
        if self.game.is_draw():
            self.game_over = True
            self.winner = 'Draw'
            return True, "Draw!"
        
        return True, f"AI played at {ai_move}"
    
    def undo_move(self):
        """Undo last human move"""
        if len(self.game.move_history) >= 2:
            # Remove AI move
            row, col, _ = self.game.move_history.pop()
            self.game.board[row][col] = ''
            
            # Remove human move
            row, col, _ = self.game.move_history.pop()
            self.game.board[row][col] = ''
            
            return True
        
        return False

# Usage
game = GameController(difficulty='hard')

print("Starting Tic Tac Toe")
game.game.print_board()

success, msg = game.play_round(0, 0)
print(f"{msg}\n")
game.game.print_board()
```

## Time Complexity Analysis

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| **Make Move** | O(1) | Direct array access |
| **Check Winner** | O(size) | Check rows, cols, diagonals |
| **Get Moves** | O(size²) | Iterate all cells |
| **Minimax** | O(b^d) | b=branching, d=depth |
| **Minimax + Pruning** | O(b^(d/2)) | Best case |

## Interview Questions

1. **How to optimize AI?**
   - Alpha-beta pruning, memoization, move ordering

2. **Extend to 4x4 board?**
   - Same logic, slower AI (exponential growth)
   - Need more aggressive pruning

3. **Handle multiplayer?**
   - Use game server, maintain game state, WebSocket for real-time

4. **Save/Load game?**
   - Serialize board and move history to JSON

5. **Why minimax?**
   - Assumes optimal play from both players
   - Best for small, deterministic games

## Key Points

- ✅ State machine for game flow
- ✅ Minimax for optimal play
- ✅ Alpha-beta pruning for performance
- ✅ Memoization for repeated states
- ✅ Strategic heuristics for difficulty levels
- ✅ Clear separation of game logic and UI
