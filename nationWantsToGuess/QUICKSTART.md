# Nation Wants to Guess - Quick Start Guide

## Windows Quick Start (5 minutes)

### Step 1: Install Python Dependencies
Open PowerShell/Command Prompt and run:
```powershell
cd C:\Users\esha.varma\EV\test\pyCraft\nationWantsToGuess
pip install -r requirements.txt
```

### Step 2: Run the App
```powershell
cd frontend
python main.py
```

**That's it!** The app will:
1. Start the FastAPI backend automatically
2. Open the Kivy UI
3. Create the SQLite database on first run

---

## Using the App

### Game Flow
1. **Enter Player Names** (3 players)
   - Type each player's name
   - Click "Start Game"

2. **Score During Game**
   - Quick buttons: +10, +20, +5, -5, -10
   - Custom input: Enter any number and click "Add"
   - Comments: Type a note and click "Comment"

3. **End Game**
   - Click "End Game & Export"
   - View final scores
   - Click "Export as CSV" to save results
   - CSV file saves to: `C:\Users\<username>\Downloads\`

---

## Troubleshooting

### Problem: "Connection error" on app startup
**Solution:** 
- Make sure port 8000 is free (not used by another app)
- Try running the backend manually:
  ```powershell
  cd backend
  uvicorn main:app --reload --host 127.0.0.1 --port 8000
  ```

### Problem: "ModuleNotFoundError" for Kivy/FastAPI
**Solution:**
```powershell
pip install kivy kivymd fastapi uvicorn sqlalchemy requests
```

### Problem: Database locked error
**Solution:**
- Close all instances of the app
- Delete `database/scoring.db`
- Restart the app (new database will be created)

---

## Manual Backend Start (if auto-start fails)

**Terminal 1 - Backend:**
```powershell
cd C:\Users\esha.varma\EV\test\pyCraft\nationWantsToGuess\backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd C:\Users\esha.varma\EV\test\pyCraft\nationWantsToGuess\frontend
python main.py
```

---

## Scoring System Explanation

| Button | Use Case |
|--------|----------|
| +10 | Correct answer / Good performance |
| +20 | Bonus points / Exceptional answer |
| +5 | Partial correct / Average performance |
| -5 | Minor mistake |
| -10 | Wrong answer / Major error |

**Custom Input:** Use the text field to enter any custom score value.

---

## Where Data is Stored

- **Database:** `C:\Users\esha.varma\EV\test\pyCraft\nationWantsToGuess\database\scoring.db`
- **Exports:** `C:\Users\<username>\Downloads\game_*.csv`

All data is stored locally (offline-first design).

---

## Building APK for Android

Requires: Java, Android SDK, NDK
```powershell
pip install buildozer
buildozer android debug
```

APK location: `bin\nation_wants_to_guess-0.1-debug.apk`

---

## Learning & Customization

### Modify Scoring Buttons
Edit `frontend/main.py`, line ~250 (search for `buttons_config`)

### Change Database Location
Edit `backend/database.py`, line ~17

### Customize UI Colors
Edit `frontend/main.py`, look for `background_color` parameters

### Add More Players
Modify `GameStart` model in `backend/main.py` to accept N players

---

## File Structure Reference

```
nationWantsToGuess/
├── backend/main.py       = API server
├── backend/database.py   = Database setup
├── frontend/main.py      = UI app
├── database/scoring.db   = Game data (auto-created)
├── requirements.txt      = Python packages
├── README.md            = Full documentation
└── buildozer.spec       = Android build config
```

---

## Need Help?

Check console output for error messages. Most issues are:
1. Missing Python packages → Run `pip install -r requirements.txt`
2. Port 8000 in use → Kill other app using port 8000
3. Database permission issues → Run as administrator or reset database
