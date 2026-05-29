# Nation Wants to Guess Scoring System

A fun, interactive game show scoring app built with Python, FastAPI, and Kivy.

## Features

- **3-Player Scoring**: Track scores for 3 simultaneous players
- **Quick Score Buttons**: Preset buttons (+10, +20, +5, -5, -10) for fast scoring
- **Custom Input**: Enter any custom score value
- **Comments**: Add comments/notes for each player
- **Offline Mode**: Works completely offline with local SQLite database
- **CSV Export**: Export final game results and score history
- **Cross-Platform**: Works on Windows, Mac, Linux, and Android

## Project Structure

```
nationWantsToGuess/
├── backend/
│   ├── __init__.py
│   ├── main.py           # FastAPI app with API endpoints
│   └── database.py       # SQLAlchemy models and SQLite setup
├── frontend/
│   ├── __init__.py
│   └── main.py          # Kivy UI application
├── database/            # SQLite database location
├── requirements.txt     # Python dependencies
└── buildozer.spec      # Android APK build configuration (to be created)
```

## Installation & Setup

### 1. Prerequisites
- Python 3.8+
- pip (Python package manager)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

**Option A: Run Frontend Only (recommended for quick start)**
```bash
cd nationWantsToGuess/frontend
python main.py
```
The frontend will automatically start the backend server.

**Option B: Run Backend and Frontend Separately**

Terminal 1 - Backend:
```bash
cd nationWantsToGuess/backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2 - Frontend:
```bash
cd nationWantsToGuess/frontend
python main.py
```

## Usage

1. **Start a Game**: Enter 3 player names and click "Start Game"
2. **Score Points**: 
   - Use quick score buttons (+10, +20, +5, -5, -10)
   - Or enter custom values in the input field
3. **Add Comments**: Write notes about each player's performance
4. **End Game**: Click "End Game & Export" when finished
5. **Export Results**: Save final scores and history as CSV

## API Endpoints

The backend provides the following REST API:

### Game Management
- `POST /game/start` - Start a new game
- `GET /games` - List all games
- `GET /game/{id}` - Get game details
- `POST /game/{id}/complete` - Mark game as complete

### Scoring
- `POST /game/{id}/score` - Add score for a player
- `GET /game/{id}/scores` - Get all scores in a game

### Comments
- `POST /game/{id}/comment` - Add a comment
- `GET /game/{id}/comments` - Get all comments

### Export
- `GET /game/{id}/export/csv` - Export game as CSV

## Database

The app uses SQLite for offline persistence. The database file is located at:
```
nationWantsToGuess/database/scoring.db
```

Tables:
- **games**: Game sessions
- **players**: Players in each game
- **scores**: Individual score entries
- **comments**: Player comments/notes

## Building for Android (APK)

To build an APK for Android deployment, use Buildozer (requires Android SDK):

```bash
# Install Buildozer
pip install buildozer

# Build APK
buildozer android debug

# The APK will be in:
# bin/nation_wants_to_guess-0.1-debug.apk
```

### Prerequisites for Android Build
- Java Development Kit (JDK)
- Android SDK
- Android NDK

See [Buildozer Documentation](https://buildozer.readthedocs.io/) for detailed setup.

## Building for Windows Desktop (EXE)

To create a standalone Windows executable:

```bash
pip install pyinstaller

pyinstaller --onefile --windowed --add-data "backend:backend" frontend/main.py
```

## Scoring System

**Default Quick Buttons:**
- `+10` Correct answer / Good performance
- `+20` Bonus / Exceptional answer
- `+5` Partial / Moderate performance
- `-5` Minor mistake
- `-10` Wrong answer / Major error

All values are customizable via the custom input field.

## Troubleshooting

### Backend won't start
- Make sure port 8000 is not in use
- Check that FastAPI and Uvicorn are installed: `pip install fastapi uvicorn`

### Kivy UI issues
- Ensure KivyMD is installed: `pip install kivymd`
- On Linux, you may need: `sudo apt-get install python3-kivy`

### Database errors
- Delete `database/scoring.db` to reset the database
- Ensure the `database/` folder has write permissions

## Future Enhancements

- [ ] Team mode (multiple teams)
- [ ] Leaderboards
- [ ] Game templates with custom rules
- [ ] Sound effects and animations
- [ ] Mobile-optimized UI
- [ ] Cloud sync option
- [ ] Multi-round tournaments

## License

Open source - feel free to modify and distribute.

## Support

For issues or questions, check the console output for error messages.
