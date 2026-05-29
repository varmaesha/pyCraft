"""
FastAPI backend for Nation Wants to Guess scoring app.
Provides offline-capable REST API for game management, scoring, and data export.
"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import csv
import io
from pydantic import BaseModel
from typing import List, Optional

from database import init_db, get_db, Game, Player, Score, Comment, Round

# Initialize database
init_db()

app = FastAPI(title="Nation Wants to Guess Scoring API")


# ============ Pydantic Models (Request/Response schemas) ============

class PlayerCreate(BaseModel):
    name: str
    position: int  # 1, 2, 3


class PlayerResponse(BaseModel):
    id: int
    name: str
    position: int
    total_score: float
    
    class Config:
        from_attributes = True


class RoundResponse(BaseModel):
    id: int
    round_number: int
    round_name: str
    started_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ScoreCreate(BaseModel):
    player_id: int
    round_number: int
    points: float


class ScoreResponse(BaseModel):
    id: int
    player_id: int
    round_number: int
    points: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    player_id: int
    text: str


class CommentResponse(BaseModel):
    id: int
    player_id: int
    text: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class GameStart(BaseModel):
    player_names: List[str]  # List of 3 player names
    game_name: Optional[str] = "Game Session"


class GameResponse(BaseModel):
    id: int
    name: str
    status: str
    current_round: int
    created_at: datetime
    completed_at: Optional[datetime]
    players: List[PlayerResponse]
    rounds: List[RoundResponse]
    
    class Config:
        from_attributes = True


class GameDetailResponse(BaseModel):
    id: int
    name: str
    status: str
    current_round: int
    created_at: datetime
    completed_at: Optional[datetime]
    players: List[PlayerResponse]
    rounds: List[RoundResponse]
    scores: List[ScoreResponse]
    comments: List[CommentResponse]
    
    class Config:
        from_attributes = True


# ============ API Endpoints ============

@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"message": "Nation Wants to Guess Scoring API is running", "version": "1.0"}


# -------- Game Management --------

@app.post("/game/start", response_model=GameResponse)
def start_game(game_start: GameStart, db: Session = Depends(get_db)):
    """Start a new game session with 3 players and 3 rounds."""
    if len(game_start.player_names) != 3:
        raise HTTPException(status_code=400, detail="Exactly 3 player names required")
    
    # Create game
    game = Game(
        name=game_start.game_name or "Game Session",
        status="active",
        current_round=1
    )
    db.add(game)
    db.flush()
    
    # Create players
    for position, name in enumerate(game_start.player_names, start=1):
        player = Player(game_id=game.id, name=name, position=position, total_score=0.0)
        db.add(player)
    
    # Create 3 rounds
    rounds_config = [
        (1, "True Story"),
        (2, "Pick Me Behavior"),
        (3, "Who Am I")
    ]
    
    for round_num, round_name in rounds_config:
        round_obj = Round(game_id=game.id, round_number=round_num, round_name=round_name)
        db.add(round_obj)
    
    db.commit()
    db.refresh(game)
    return game


@app.get("/games", response_model=List[GameResponse])
def list_games(db: Session = Depends(get_db)):
    """List all game sessions."""
    games = db.query(Game).order_by(Game.created_at.desc()).all()
    return games


@app.get("/game/{game_id}", response_model=GameDetailResponse)
def get_game(game_id: int, db: Session = Depends(get_db)):
    """Get detailed game information including scores and comments."""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@app.post("/game/{game_id}/next-round", response_model=GameDetailResponse)
def next_round(game_id: int, db: Session = Depends(get_db)):
    """Advance game to next round."""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if game.current_round >= 3:
        raise HTTPException(status_code=400, detail="Already on last round")
    
    game.current_round += 1
    db.commit()
    db.refresh(game)
    return game


@app.post("/game/{game_id}/complete", response_model=GameDetailResponse)
def complete_game(game_id: int, db: Session = Depends(get_db)):
    """Mark game as completed."""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game.status = "completed"
    game.completed_at = datetime.now()
    db.commit()
    db.refresh(game)
    return game


# -------- Scoring --------

@app.post("/game/{game_id}/score", response_model=ScoreResponse)
def add_score(game_id: int, score_data: ScoreCreate, db: Session = Depends(get_db)):
    """Add a score for a player in a specific round."""
    # Validate game exists
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Validate player exists and belongs to game
    player = db.query(Player).filter(
        Player.id == score_data.player_id,
        Player.game_id == game_id
    ).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found in this game")
    
    # Validate round number
    if score_data.round_number not in [1, 2, 3]:
        raise HTTPException(status_code=400, detail="Invalid round number")
    
    # Create score entry
    score = Score(
        game_id=game_id,
        player_id=score_data.player_id,
        round_number=score_data.round_number,
        points=score_data.points
    )
    db.add(score)
    
    # Update player's total score
    player.total_score += score_data.points
    
    db.commit()
    db.refresh(score)
    return score


@app.get("/game/{game_id}/scores", response_model=List[ScoreResponse])
def get_game_scores(game_id: int, db: Session = Depends(get_db)):
    """Get all scores for a game."""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    scores = db.query(Score).filter(Score.game_id == game_id).order_by(Score.created_at).all()
    return scores


# -------- Comments --------

@app.post("/game/{game_id}/comment", response_model=CommentResponse)
def add_comment(game_id: int, comment_data: CommentCreate, db: Session = Depends(get_db)):
    """Add a comment for a player."""
    # Validate game and player exist
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    player = db.query(Player).filter(
        Player.id == comment_data.player_id,
        Player.game_id == game_id
    ).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found in this game")
    
    # Create comment
    comment = Comment(
        game_id=game_id,
        player_id=comment_data.player_id,
        text=comment_data.text
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@app.get("/game/{game_id}/comments", response_model=List[CommentResponse])
def get_game_comments(game_id: int, db: Session = Depends(get_db)):
    """Get all comments for a game."""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    comments = db.query(Comment).filter(Comment.game_id == game_id).order_by(Comment.created_at).all()
    return comments


# -------- Export --------

@app.get("/game/{game_id}/export/csv")
def export_game_csv(game_id: int, db: Session = Depends(get_db)):
    """Export game data as CSV with round-by-round breakdown."""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Generate CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(["Nation Wants to Guess - Game Report"])
    writer.writerow(["Game Name", game.name])
    writer.writerow(["Created At", game.created_at.strftime('%Y-%m-%d %H:%M:%S')])
    writer.writerow(["Status", game.status])
    writer.writerow([])
    
    # Round-by-round breakdown
    rounds = db.query(Round).filter(Round.game_id == game_id).order_by(Round.round_number).all()
    for round_obj in rounds:
        writer.writerow([f"Round {round_obj.round_number}: {round_obj.round_name}"])
        writer.writerow(["Player", "Points"])
        
        scores = db.query(Score).filter(
            (Score.game_id == game_id) & (Score.round_number == round_obj.round_number)
        ).order_by(Score.player_id).all()
        
        # Group scores by player
        player_round_scores = {}
        for score in scores:
            if score.player_id not in player_round_scores:
                player_round_scores[score.player_id] = 0
            player_round_scores[score.player_id] += score.points
        
        # Write scores for this round
        for player in game.players:
            round_score = player_round_scores.get(player.id, 0)
            writer.writerow([player.name, round_score])
        
        writer.writerow([])
    
    # Player Final Scores
    writer.writerow(["Final Standings"])
    writer.writerow(["Rank", "Player Name", "Final Score"])
    sorted_players = sorted(game.players, key=lambda p: p.total_score, reverse=True)
    for rank, player in enumerate(sorted_players, 1):
        writer.writerow([rank, player.name, player.total_score])
    
    writer.writerow([])
    
    # Score Details
    writer.writerow(["All Score Entries"])
    writer.writerow(["Player", "Round", "Points", "Timestamp"])
    scores = db.query(Score).filter(Score.game_id == game_id).order_by(Score.created_at).all()
    for score in scores:
        player = db.query(Player).filter(Player.id == score.player_id).first()
        round_obj = db.query(Round).filter(
            (Round.game_id == game_id) & (Round.round_number == score.round_number)
        ).first()
        round_name = round_obj.round_name if round_obj else "Unknown"
        writer.writerow([player.name, round_name, score.points, score.created_at.strftime('%Y-%m-%d %H:%M:%S')])
    
    writer.writerow([])
    
    # Comments
    if db.query(Comment).filter(Comment.game_id == game_id).count() > 0:
        writer.writerow(["Comments"])
        writer.writerow(["Player", "Comment", "Timestamp"])
        comments = db.query(Comment).filter(Comment.game_id == game_id).order_by(Comment.created_at).all()
        for comment in comments:
            player = db.query(Player).filter(Player.id == comment.player_id).first()
            writer.writerow([player.name, comment.text, comment.created_at.strftime('%Y-%m-%d %H:%M:%S')])
    
    csv_content = output.getvalue()
    return {
        "filename": f"game_{game_id}_export.csv",
        "content": csv_content,
        "status": "success"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
