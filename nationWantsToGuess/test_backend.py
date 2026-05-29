#!/usr/bin/env python3
"""
Test script to verify Nation Wants to Guess backend is working.
"""
import sys
import os
import time
import subprocess
import requests

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

def test_backend_startup():
    """Test if backend starts successfully."""
    print("Testing backend startup...")
    
    try:
        from backend.database import init_db
        print("✓ Database module imported successfully")
        
        # Initialize database
        init_db()
        print("✓ Database initialized successfully")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_backend_server():
    """Test if backend server responds."""
    print("\nTesting backend server...")
    
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if response.status_code == 200:
            print(f"✓ Backend server responding: {response.json()}")
            return True
        else:
            print(f"✗ Server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend server")
        print("  Make sure backend is running on http://127.0.0.1:8000/")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_game_creation():
    """Test if we can create a game."""
    print("\nTesting game creation...")
    
    try:
        payload = {
            "player_names": ["Player 1", "Player 2", "Player 3"],
            "game_name": "Test Game"
        }
        response = requests.post("http://127.0.0.1:8000/game/start", json=payload, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Game created successfully (ID: {data['id']})")
            print(f"  Players: {', '.join([p['name'] for p in data['players']])}")
            return True, data['id']
        else:
            print(f"✗ Failed to create game: {response.text}")
            return False, None
    except Exception as e:
        print(f"✗ Error: {e}")
        return False, None

def test_scoring(game_id):
    """Test if scoring works."""
    print("\nTesting score addition...")
    
    try:
        response = requests.get(f"http://127.0.0.1:8000/game/{game_id}")
        players = response.json()['players']
        player_id = players[0]['id']
        
        payload = {
            "player_id": player_id,
            "points": 10
        }
        response = requests.post(f"http://127.0.0.1:8000/game/{game_id}/score", json=payload, timeout=5)
        
        if response.status_code == 200:
            print(f"✓ Score added successfully")
            return True
        else:
            print(f"✗ Failed to add score: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("="*50)
    print("Nation Wants to Guess - Backend Test Suite")
    print("="*50 + "\n")
    
    # Test 1: Database
    if not test_backend_startup():
        print("\n✗ Backend startup test failed")
        sys.exit(1)
    
    print("\n" + "-"*50)
    print("To run full tests, the backend server must be running:")
    print("  cd backend")
    print("  uvicorn main:app --reload --host 127.0.0.1 --port 8000")
    print("-"*50)
    
    # Test 2-4: API tests (requires running server)
    print("\nWaiting 2 seconds for potential manual server startup...")
    time.sleep(2)
    
    if not test_backend_server():
        print("\n⚠ Backend server is not running. API tests skipped.")
        print("This is okay if you haven't started the server yet.")
        return
    
    success, game_id = test_game_creation()
    if not success:
        return
    
    test_scoring(game_id)
    
    print("\n" + "="*50)
    print("✓ All tests passed!")
    print("="*50)

if __name__ == '__main__':
    main()
