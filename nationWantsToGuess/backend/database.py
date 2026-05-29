"""
Database configuration and models for Nation Wants to Guess scoring app.
SQLite database for offline-first scoring system.
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database path (in the database folder)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'scoring.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Game(Base):
    """Represents a single game session with 3 rounds."""
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="Game Session")
    status = Column(String, default="active")  # active, completed
    current_round = Column(Integer, default=1)  # 1, 2, or 3
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    players = relationship("Player", back_populates="game", cascade="all, delete-orphan")
    rounds = relationship("Round", back_populates="game", cascade="all, delete-orphan")
    scores = relationship("Score", back_populates="game", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="game", cascade="all, delete-orphan")


class Round(Base):
    """Represents a single round in a game."""
    __tablename__ = "rounds"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    round_number = Column(Integer, nullable=False)  # 1, 2, 3
    round_name = Column(String, nullable=False)  # "True Story", "Pick Me Behavior", "Who Am I"
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    game = relationship("Game", back_populates="rounds")


class Player(Base):
    """Represents a player in a game."""
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    name = Column(String, nullable=False)
    position = Column(Integer)  # 1, 2, or 3 for display order
    total_score = Column(Float, default=0.0)
    
    game = relationship("Game", back_populates="players")
    scores = relationship("Score", back_populates="player", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="player", cascade="all, delete-orphan")


class Score(Base):
    """Represents a single score entry for a player in a specific round."""
    __tablename__ = "scores"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    round_number = Column(Integer, nullable=False)  # 1, 2, or 3
    points = Column(Float, nullable=False)  # Can be positive or negative
    created_at = Column(DateTime, default=datetime.utcnow)
    
    game = relationship("Game", back_populates="scores")
    player = relationship("Player", back_populates="scores")


class Comment(Base):
    """Represents a comment/note for a player or round."""
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    game = relationship("Game", back_populates="comments")
    player = relationship("Player", back_populates="comments")


def init_db():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
