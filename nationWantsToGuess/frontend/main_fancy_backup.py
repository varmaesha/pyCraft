"""
Kivy frontend for Nation Wants to Guess scoring app - IMPROVED UI
Minimal UI design with 3-player scoring, custom inputs, and CSV export.
Dark mode with leaderboard, animated scores, and better visual hierarchy.
"""
import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation
import requests
import json
from datetime import datetime
import subprocess
import threading

# Set window size for desktop testing
Window.size = (1000, 900)

# Backend URL (local FastAPI server)
BACKEND_URL = "http://127.0.0.1:8000"

# Color scheme - Dark Mode
DARK_BG = (0.15, 0.15, 0.18, 1)      # Very dark gray-blue
DARKER_BG = (0.1, 0.1, 0.12, 1)      # Even darker
ACCENT_COLOR = (0.0, 0.7, 1.0, 1)    # Bright cyan
ACCENT_DARK = (0.0, 0.5, 0.8, 1)     # Darker cyan
POSITIVE = (0.0, 0.8, 0.4, 1)        # Green for positive scores
NEGATIVE = (1.0, 0.3, 0.3, 1)        # Red for negative scores
TEXT_COLOR = (0.95, 0.95, 0.95, 1)   # Light gray-white
TEXT_SECONDARY = (0.7, 0.7, 0.75, 1) # Medium gray


class NationWantsToGuessApp(App):
    """Main Kivy application for Nation Wants to Guess scoring."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_game = None
        self.players = []
        self.player_widgets = {}
    
    def build(self):
        """Build the main app UI."""
        self.title = "Nation Wants to Guess - Scoring System"
        
        # Set dark theme
        Window.clearcolor = DARK_BG
        
        self.root = BoxLayout(orientation='vertical', padding=0, spacing=0)
        
        # Show player entry screen
        self.show_player_entry_screen()
        
        return self.root
    
    def on_start(self):
        """Initialize app - backend must be running separately."""
        print("✓ Kivy app started (Dark Mode)")
        print(f"Attempting to connect to backend at {BACKEND_URL}")
        self.check_backend_connection()
    
    def check_backend_connection(self):
        """Verify backend server is running."""
        try:
            response = requests.get(f"{BACKEND_URL}/", timeout=2)
            print(f"✓ Backend connected: {response.json()}")
        except requests.exceptions.ConnectionError:
            print(f"✗ Backend not running at {BACKEND_URL}")
            print("Start the backend first:")
            print("  cd backend")
            print("  uvicorn main:app --reload --host 127.0.0.1 --port 8000")
        except Exception as e:
            print(f"⚠ Connection check error: {e}")
    
    def show_player_entry_screen(self):
        """Display screen for entering 3 player names."""
        self.root.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # Header
        header = Label(
            text='[b][size=40]Nation Wants to Guess[/size][/b]\n[size=16]Scoring System[/size]',
            markup=True,
            color=TEXT_COLOR,
            size_hint_y=0.2
        )
        layout.add_widget(header)
        
        divider = Label(size_hint_y=0.05)
        layout.add_widget(divider)
        
        # Player inputs
        title_label = Label(
            text='Enter Player Names',
            color=ACCENT_COLOR,
            size_hint_y=0.08,
            font_size='18sp',
            bold=True
        )
        layout.add_widget(title_label)
        
        self.player_inputs = []
        for i in range(3):
            player_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=15)
            
            label = Label(
                text=f'Player {i+1}:',
                size_hint_x=0.2,
                color=TEXT_COLOR,
                font_size='14sp'
            )
            player_layout.add_widget(label)
            
            text_input = TextInput(
                text=f'Player {i+1}',
                multiline=False,
                size_hint_x=0.8,
                background_color=DARKER_BG,
                foreground_color=TEXT_COLOR,
                font_size='14sp',
                padding=[10, 10]
            )
            # Draw rounded rectangle border
            with text_input.canvas.before:
                Color(ACCENT_COLOR[0], ACCENT_COLOR[1], ACCENT_COLOR[2], 0.3)
                text_input.rect = RoundedRectangle(size=text_input.size, pos=text_input.pos, radius=[10])
            text_input.bind(size=lambda *args: setattr(text_input.rect, 'size', text_input.size),
                           pos=lambda *args: setattr(text_input.rect, 'pos', text_input.pos))
            
            self.player_inputs.append(text_input)
            player_layout.add_widget(text_input)
            layout.add_widget(player_layout)
        
        # Buttons
        button_layout = BoxLayout(size_hint_y=0.25, spacing=15)
        
        start_button = self.create_button('Start Game', ACCENT_COLOR, lambda x: self.start_game(x))
        button_layout.add_widget(start_button)
        
        load_button = self.create_button('Load Previous', TEXT_SECONDARY, lambda x: self.show_load_games_screen(x))
        button_layout.add_widget(load_button)
        
        layout.add_widget(button_layout)
        
        self.root.add_widget(layout)
    
    def create_button(self, text, color, callback):
        """Create a styled button."""
        btn = Button(text=text, font_size='14sp', bold=True)
        btn.background_color = color
        btn.bind(on_press=callback)
        return btn
    
    def start_game(self, instance):
        """Create a new game session with entered player names."""
        player_names = [inp.text for inp in self.player_inputs]
        
        if any(not name.strip() for name in player_names):
            self.show_popup('Error', 'All player names are required!')
            return
        
        try:
            print(f"Starting game with players: {player_names}")
            payload = {
                "player_names": player_names,
                "game_name": f"Game - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            }
            response = requests.post(f"{BACKEND_URL}/game/start", json=payload)
            
            if response.status_code == 200:
                self.current_game = response.json()
                self.players = self.current_game['players']
                print(f"✓ Game started with ID: {self.current_game['id']}")
                self.show_scoring_screen()
            else:
                error_msg = f"Status {response.status_code}: {response.text}"
                print(f"✗ Failed to start game: {error_msg}")
                self.show_popup('Error', f"Failed to start game:\n{error_msg}")
        except Exception as e:
            print(f"✗ Start game error: {e}")
            self.show_popup('Error', f"Connection error: {str(e)}\n\nMake sure backend is running!")
    
    def show_scoring_screen(self):
        """Display the main scoring screen with 3 player cards, leaderboard, and past rounds summary."""
        self.root.clear_widgets()
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # ====== HEADER with Round Info ======
        header_layout = BoxLayout(size_hint_y=0.12, spacing=10, padding=10, orientation='vertical')
        
        # Top row: Game title and controls
        top_row = BoxLayout(size_hint_y=0.5, spacing=10)
        
        game_title = Label(
            text=self.current_game['name'],
            color=ACCENT_COLOR,
            font_size='16sp',
            bold=True,
            size_hint_x=0.4
        )
        top_row.add_widget(game_title)
        
        menu_btn = Button(text='Menu', size_hint_x=0.12, background_color=(0.5, 0.2, 0.2, 1))
        menu_btn.bind(on_press=self.show_menu)
        top_row.add_widget(menu_btn)
        
        # Next Round button (prominent)
        current_round = self.current_game.get('current_round', 1)
        if current_round < 3:
            next_round_btn = Button(
                text=f'🏁 Finish Round {current_round}',
                size_hint_x=0.25,
                background_color=ACCENT_COLOR,
                font_size='12sp',
                bold=True
            )
            next_round_btn.bind(on_press=self.advance_to_next_round)
            top_row.add_widget(next_round_btn)
        
        end_btn = Button(text='End Game', size_hint_x=0.12, background_color=POSITIVE)
        end_btn.bind(on_press=self.end_game)
        top_row.add_widget(end_btn)
        
        header_layout.add_widget(top_row)
        
        # Bottom row: Round info
        round_info = self.current_game.get('rounds', [])
        current_round = self.current_game.get('current_round', 1)
        round_name = round_info[current_round - 1]['round_name'] if current_round <= len(round_info) else "Unknown"
        
        round_row = BoxLayout(size_hint_y=0.5, spacing=10)
        
        round_label = Label(
            text=f"[b]Round {current_round}: {round_name}[/b]",
            color=ACCENT_COLOR,
            markup=True,
            font_size='14sp',
            size_hint_x=0.7
        )
        round_row.add_widget(round_label)
        
        # Round progress indicators
        for i in range(1, 4):
            indicator_color = POSITIVE if i <= current_round else (0.4, 0.4, 0.4, 1)
            indicator_label = Label(
                text=f"{i}",
                color=indicator_color,
                font_size='12sp',
                size_hint_x=0.1
            )
            round_row.add_widget(indicator_label)
        
        header_layout.add_widget(round_row)
        main_layout.add_widget(header_layout)
        
        # ====== MAIN CONTENT (2 columns) - Player cards and leaderboard ======
        content_layout = BoxLayout(orientation='horizontal', spacing=10, padding=8, size_hint_y=0.55)
        
        # LEFT: Player scoring cards (compact)
        left_panel = BoxLayout(orientation='vertical', spacing=6, size_hint_x=0.6)
        
        for player in self.players:
            card = self.create_player_card(player)
            left_panel.add_widget(card)
        
        content_layout.add_widget(left_panel)
        
        # RIGHT: Leaderboard
        right_panel = self.create_leaderboard()
        content_layout.add_widget(right_panel)
        
        main_layout.add_widget(content_layout)
        
        # ====== PAST ROUNDS SUMMARY ======
        if current_round > 1:
            past_rounds_section = self.create_past_rounds_section()
            main_layout.add_widget(past_rounds_section)
        
        self.root.add_widget(main_layout)
        
        self.refresh_game_state()
    
    def create_player_card(self, player):
        """Create a compact player card with score display."""
        card = BoxLayout(orientation='vertical', size_hint_y=None, height=85, padding=8, spacing=4)
        
        # Header with name and score (single line)
        header = BoxLayout(size_hint_y=0.25, spacing=8)
        
        name_label = Label(
            text=player['name'],
            color=TEXT_COLOR,
            size_hint_x=0.5,
            font_size='13sp',
            bold=True
        )
        header.add_widget(name_label)
        
        score_color = POSITIVE if player['total_score'] >= 0 else NEGATIVE
        score_label = Label(
            text=f"{player['total_score']:.0f}",
            color=score_color,
            size_hint_x=0.5,
            font_size='16sp',
            bold=True
        )
        header.add_widget(score_label)
        
        card.add_widget(header)
        
        # Quick buttons (1 row)
        buttons_layout = GridLayout(cols=5, size_hint_y=0.4, spacing=3)
        buttons_config = [('+10', 10), ('+20', 20), ('+5', 5), ('-5', -5), ('-10', -10)]
        
        for btn_text, points in buttons_config:
            btn = Button(text=btn_text, font_size='9sp')
            btn_color = POSITIVE if points > 0 else NEGATIVE
            btn.background_color = btn_color
            btn.bind(on_press=lambda x, p=player['id'], pts=points: self.add_score(p, pts))
            buttons_layout.add_widget(btn)
        
        card.add_widget(buttons_layout)
        
        # Input row (compact)
        input_row = BoxLayout(size_hint_y=0.35, spacing=3)
        
        # Custom score input
        custom_input = TextInput(
            text='0',
            multiline=False,
            input_filter='float',
            size_hint_x=0.25,
            background_color=DARKER_BG,
            foreground_color=TEXT_COLOR,
            font_size='10sp'
        )
        input_row.add_widget(custom_input)
        
        add_btn = Button(text='Add', size_hint_x=0.15, background_color=ACCENT_COLOR, font_size='9sp')
        def add_custom(btn, player_id, inp):
            try:
                points = float(inp.text) if inp.text else 0
                self.add_score(player_id, points)
                inp.text = '0'
            except ValueError:
                self.show_popup('Error', 'Invalid number')
        add_btn.bind(on_press=lambda x, p=player['id'], inp=custom_input: add_custom(x, p, inp))
        input_row.add_widget(add_btn)
        
        # Comment input
        comment_input = TextInput(
            hint_text='Comment...',
            multiline=False,
            size_hint_x=0.45,
            background_color=DARKER_BG,
            foreground_color=TEXT_COLOR,
            hint_text_color=TEXT_SECONDARY,
            font_size='9sp'
        )
        input_row.add_widget(comment_input)
        
        comment_btn = Button(text='💬', size_hint_x=0.15, background_color=ACCENT_DARK, font_size='10sp')
        def add_comment_fn(btn, player_id, comment_field):
            self.add_comment(player_id, comment_field.text)
            comment_field.text = ''
        comment_btn.bind(on_press=lambda x, p=player['id'], c=comment_input: add_comment_fn(x, p, c))
        input_row.add_widget(comment_btn)
        
        card.add_widget(input_row)
        
        # Draw card background
        with card.canvas.before:
            Color(DARKER_BG[0], DARKER_BG[1], DARKER_BG[2], 1)
            card.rect = RoundedRectangle(size=card.size, pos=card.pos, radius=[15])
        card.bind(size=lambda *args: setattr(card.rect, 'size', card.size),
                 pos=lambda *args: setattr(card.rect, 'pos', card.pos))
        
        self.player_widgets[player['id']] = {
            'card': card,
            'score_label': score_label,
            'name_label': name_label
        }
        
        return card
    
    def create_leaderboard(self):
        """Create a leaderboard panel showing live rankings."""
        panel = BoxLayout(orientation='vertical', size_hint_x=0.4, padding=6, spacing=6)
        
        title = Label(
            text='LEADERBOARD',
            color=ACCENT_COLOR,
            size_hint_y=0.08,
            font_size='11sp',
            bold=True
        )
        panel.add_widget(title)
        
        self.leaderboard_container = BoxLayout(orientation='vertical', size_hint_y=0.92, spacing=3)
        
        # Sort players by score
        sorted_players = sorted(self.players, key=lambda p: p['total_score'], reverse=True)
        
        for idx, player in enumerate(sorted_players, 1):
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=30, spacing=6)
            
            # Rank
            rank_label = Label(
                text=f"{idx}.",
                color=ACCENT_COLOR,
                size_hint_x=0.15,
                font_size='12sp',
                bold=True
            )
            row.add_widget(rank_label)
            
            # Player name
            name_label = Label(
                text=player['name'],
                color=TEXT_COLOR,
                size_hint_x=0.45,
                font_size='11sp'
            )
            row.add_widget(name_label)
            
            # Score
            score_color = POSITIVE if player['total_score'] >= 0 else NEGATIVE
            score_label = Label(
                text=f"{player['total_score']:.0f}",
                color=score_color,
                size_hint_x=0.4,
                font_size='12sp',
                bold=True
            )
            row.add_widget(score_label)
            
            # Draw row background (alternating)
            with row.canvas.before:
                if idx % 2 == 0:
                    Color(0.18, 0.18, 0.22, 1)
                else:
                    Color(0.12, 0.12, 0.14, 1)
                row.rect = RoundedRectangle(size=row.size, pos=row.pos, radius=[5])
            row.bind(size=lambda *args: setattr(row.rect, 'size', row.size),
                    pos=lambda *args: setattr(row.rect, 'pos', row.pos))
            
            self.leaderboard_container.add_widget(row)
        
        panel.add_widget(self.leaderboard_container)
        
        return panel
    
    def create_past_rounds_section(self):
        """Create past rounds summary showing all players' scores."""
        current_round = self.current_game.get('current_round', 1)
        
        # If no past rounds, return empty
        if current_round <= 1:
            return BoxLayout(orientation='vertical', size_hint_y=0.05)
        
        section = BoxLayout(orientation='vertical', size_hint_y=0.15, padding=5, spacing=2)
        
        # Title
        title = Label(
            text='[b]ROUND HISTORY[/b]',
            markup=True,
            color=ACCENT_COLOR,
            size_hint_y=0.15,
            font_size='10sp',
            bold=True
        )
        section.add_widget(title)
        
        # Scrollable area
        scroll = ScrollView(size_hint_y=0.85)
        summary_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=0)
        summary_container.bind(minimum_height=summary_container.setter('height'))
        
        round_info = {r['round_number']: r['round_name'] for r in self.current_game.get('rounds', [])}
        players = self.current_game.get('players', [])
        scores = self.current_game.get('scores', [])
        
        # Build dictionary of player info for quick lookup
        player_dict = {p['id']: p['name'] for p in players}
        
        try:
            # Show all completed rounds
            for round_num in range(1, current_round):
                round_name = round_info.get(round_num, 'Unknown')
                
                # Initialize round scores for all players
                round_scores = {pid: 0 for pid in player_dict.keys()}
                
                # Sum up scores for this round
                for score_entry in scores:
                    if score_entry.get('round_number') == round_num:
                        pid = score_entry.get('player_id')
                        if pid in round_scores:
                            round_scores[pid] += score_entry.get('points', 0)
                
                # Create list of (player_id, name, score) tuples and sort
                player_scores = [(pid, player_dict[pid], round_scores[pid]) for pid in round_scores]
                player_scores.sort(key=lambda x: x[2], reverse=True)  # Sort by score descending
                
                # Build display string
                score_str_parts = []
                medals = ['🥇', '🥈', '🥉']
                
                for idx, (pid, name, score) in enumerate(player_scores):
                    medal = medals[idx] if idx < 3 else f"{idx+1}."
                    score_fmt = f"{score:+.0f}" if score != 0 else "0"
                    score_str_parts.append(f"{medal}{name}:{score_fmt}")
                
                # Create label for this round
                round_text = f"R{round_num} {round_name}  →  {' | '.join(score_str_parts)}"
                round_label = Label(
                    text=round_text,
                    color=TEXT_SECONDARY,
                    size_hint_y=None,
                    height=18,
                    font_size='8sp'
                )
                summary_container.add_widget(round_label)
        
        except Exception as e:
            print(f"Round summary error: {e}")
            error_label = Label(
                text="Error: Could not load round summary",
                color=NEGATIVE,
                size_hint_y=None,
                height=18
            )
            summary_container.add_widget(error_label)
        
        scroll.add_widget(summary_container)
        section.add_widget(scroll)
        
        return section
    
    def add_score(self, player_id, points):
        """Add score for a player."""
        try:
            print(f"Adding {points} points to player {player_id}")
            payload = {
                "player_id": player_id,
                "points": points,
                "round_number": self.current_game['current_round']
            }
            response = requests.post(f"{BACKEND_URL}/game/{self.current_game['id']}/score", json=payload)
            
            if response.status_code == 200:
                print(f"✓ Score added successfully")
                self.refresh_game_state()
                # Rebuild UI to show updated scores
                self.show_scoring_screen()
            else:
                error_msg = response.text
                print(f"✗ Failed to add score: {error_msg}")
                self.show_popup('Error', f"Failed to add score:\n{error_msg}")
        except Exception as e:
            print(f"✗ Add score error: {e}")
            self.show_popup('Error', f"Connection error: {str(e)}\n\nMake sure backend is running!")
    
    def add_comment(self, player_id, text):
        """Add a comment for a player."""
        if not text.strip():
            return
        
        try:
            print(f"Adding comment to player {player_id}: {text}")
            payload = {
                "player_id": player_id,
                "text": text
            }
            response = requests.post(f"{BACKEND_URL}/game/{self.current_game['id']}/comment", json=payload)
            
            if response.status_code == 200:
                print(f"✓ Comment added successfully")
                self.refresh_game_state()
                # Rebuild UI to show updated comments
                self.show_scoring_screen()
            else:
                error_msg = response.text
                print(f"✗ Failed to add comment: {error_msg}")
                self.show_popup('Error', f"Failed to add comment:\n{error_msg}")
        except Exception as e:
            print(f"✗ Add comment error: {e}")
            self.show_popup('Error', f"Connection error: {str(e)}")
    
    def refresh_game_state(self):
        """Refresh game state from backend and update UI."""
        try:
            response = requests.get(f"{BACKEND_URL}/game/{self.current_game['id']}")
            
            if response.status_code == 200:
                self.current_game = response.json()
                self.players = self.current_game['players']
                
                # Update UI with new scores
                for player in self.players:
                    # Find and update the player card in the UI
                    pass  # Scores will be updated on next refresh of scoring screen
                print(f"✓ Game state refreshed. Scores: {[(p['name'], p['total_score']) for p in self.players]}")
            else:
                print(f"✗ Refresh failed: {response.status_code}")
        except Exception as e:
            print(f"✗ Refresh error: {e}")
    
    def advance_to_next_round(self, instance):
        """Advance to next round and stay on same page - past rounds show below."""
        try:
            current_round = self.current_game.get('current_round', 1)
            if current_round >= 3:
                self.show_popup('Info', 'Already on final round! Click "End Game" to finish.')
                return
            
            # Call backend to advance round
            response = requests.post(f"{BACKEND_URL}/game/{self.current_game['id']}/next-round")
            
            if response.status_code == 200:
                # Update current game with full response from backend
                self.current_game = response.json()
                self.players = self.current_game.get('players', [])
                
                new_round = self.current_game['current_round']
                print(f"✓ Advanced to round {new_round}")
                
                # Rebuild the scoring screen to show past rounds
                self.show_scoring_screen()
                self.show_popup('✓ Info', f'Round {new_round} Started!')
            else:
                error_msg = response.text
                print(f"✗ Failed to advance round: {error_msg}")
                self.show_popup('Error', f"Failed to advance to next round:\n{error_msg}")
        except Exception as e:
            print(f"✗ Advance round error: {e}")
            self.show_popup('Error', f"Connection error: {str(e)}\n\nMake sure backend is running!")
    
    def end_game(self, instance):
        """Handle end game button - show final summary before completing."""
        try:
            current_round = self.current_game.get('current_round', 1)
            if current_round == 3:
                # Show final summary before game completion
                self.show_round_summary_before_end()
            else:
                self.show_popup('Info', f"Game is still in Round {current_round}.\nYou can only end after Round 3.")
        except Exception as e:
            print(f"✗ End game error: {e}")
            self.show_popup('Error', f"Error: {str(e)}")
    
    def show_round_summary(self):
        """Display summary of the current round before advancing."""
        self.root.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        current_round = self.current_game.get('current_round', 1)
        round_names = {1: "True Story", 2: "Pick Me Behavior", 3: "Who Am I"}
        title_label = Label(
            text=f"[b]ROUND {current_round}: {round_names.get(current_round, '')} - SUMMARY[/b]",
            markup=True,
            color=ACCENT_COLOR,
            size_hint_y=None,
            height=50,
            font_size='18sp'
        )
        layout.add_widget(title_label)
        
        # Scroll view for results
        scroll = ScrollView()
        results_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        results_container.bind(minimum_height=results_container.setter('height'))
        
        # Get current game data and calculate round scores
        try:
            response = requests.get(f"{BACKEND_URL}/game/{self.current_game['id']}")
            if response.status_code == 200:
                game_data = response.json()
                players = game_data.get('players', [])
                scores = game_data.get('scores', [])
                
                # Calculate scores for current round
                player_round_scores = {}
                for player in players:
                    player_round_scores[player['id']] = {
                        'name': player['name'],
                        'round_score': 0,
                        'total_score': player['total_score']
                    }
                
                for score in scores:
                    if score.get('round_number') == current_round:
                        player_id = score.get('player_id')
                        if player_id in player_round_scores:
                            player_round_scores[player_id]['round_score'] += score.get('points', 0)
                
                # Display sorted by round score (descending)
                sorted_players = sorted(
                    player_round_scores.values(),
                    key=lambda x: x['round_score'],
                    reverse=True
                )
                
                for i, player in enumerate(sorted_players, 1):
                    row_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=15)
                    
                    # Ranking
                    medals = ['🥇', '🥈', '🥉']
                    medal = medals[i-1] if i <= 3 else f"{i}."
                    rank_label = Label(
                        text=medal,
                        size_hint_x=0.1,
                        font_size='16sp'
                    )
                    row_layout.add_widget(rank_label)
                    
                    # Name
                    name_label = Label(
                        text=player['name'],
                        color=TEXT_COLOR,
                        size_hint_x=0.4,
                        font_size='14sp',
                        bold=True
                    )
                    row_layout.add_widget(name_label)
                    
                    # Round score
                    score_color = POSITIVE if player['round_score'] >= 0 else NEGATIVE
                    round_score_label = Label(
                        text=f"Round: {player['round_score']:+.0f}",
                        color=score_color,
                        size_hint_x=0.25,
                        font_size='13sp'
                    )
                    row_layout.add_widget(round_score_label)
                    
                    # Total score
                    total_label = Label(
                        text=f"Total: {player['total_score']:.0f}",
                        color=ACCENT_COLOR,
                        size_hint_x=0.25,
                        font_size='13sp',
                        bold=True
                    )
                    row_layout.add_widget(total_label)
                    
                    results_container.add_widget(row_layout)
                    
                    # Add separator
                    separator = Label(text='', size_hint_y=None, height=5)
                    results_container.add_widget(separator)
        
        except Exception as e:
            error_label = Label(text=f"Error loading scores: {str(e)}", color=NEGATIVE)
            results_container.add_widget(error_label)
        
        scroll.add_widget(results_container)
        layout.add_widget(scroll)
        
        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        next_btn = Button(
            text=f"Continue to Round {current_round + 1}" if current_round < 3 else "End Game",
            background_color=ACCENT_COLOR,
            color=(1, 1, 1, 1)
        )
        if current_round < 3:
            next_btn.bind(on_press=self.advance_to_next_round_actual)
        else:
            next_btn.bind(on_press=self.end_game_actual)
        button_layout.add_widget(next_btn)
        
        back_btn = Button(
            text="Back to Scoring",
            background_color=NEGATIVE
        )
        back_btn.bind(on_press=lambda x: self.show_scoring_screen())
        button_layout.add_widget(back_btn)
        
        layout.add_widget(button_layout)
        self.root.add_widget(layout)
    
    def show_round_summary_before_end(self):
        """Show round 3 summary before ending game."""
        self.root.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title_label = Label(
            text="[b]ROUND 3: WHO AM I - SUMMARY[/b]",
            markup=True,
            color=ACCENT_COLOR,
            size_hint_y=None,
            height=50,
            font_size='18sp'
        )
        layout.add_widget(title_label)
        
        # Scroll view for results
        scroll = ScrollView()
        results_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        results_container.bind(minimum_height=results_container.setter('height'))
        
        # Get current game data
        try:
            response = requests.get(f"{BACKEND_URL}/game/{self.current_game['id']}")
            if response.status_code == 200:
                game_data = response.json()
                players = game_data.get('players', [])
                scores = game_data.get('scores', [])
                
                # Calculate scores for round 3
                player_round_scores = {}
                for player in players:
                    player_round_scores[player['id']] = {
                        'name': player['name'],
                        'round_score': 0,
                        'total_score': player['total_score']
                    }
                
                for score in scores:
                    if score.get('round_number') == 3:
                        player_id = score.get('player_id')
                        if player_id in player_round_scores:
                            player_round_scores[player_id]['round_score'] += score.get('points', 0)
                
                # Display sorted by total score (final winner)
                sorted_players = sorted(
                    player_round_scores.values(),
                    key=lambda x: x['total_score'],
                    reverse=True
                )
                
                for i, player in enumerate(sorted_players, 1):
                    row_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=15)
                    
                    # Ranking
                    medals = ['🥇 WINNER!', '🥈', '🥉']
                    medal = medals[i-1] if i <= 3 else f"{i}."
                    rank_label = Label(
                        text=medal,
                        color=POSITIVE if i == 1 else TEXT_COLOR,
                        size_hint_x=0.15,
                        font_size='14sp',
                        bold=True
                    )
                    row_layout.add_widget(rank_label)
                    
                    # Name
                    name_label = Label(
                        text=player['name'],
                        color=ACCENT_COLOR if i == 1 else TEXT_COLOR,
                        size_hint_x=0.35,
                        font_size='14sp',
                        bold=True
                    )
                    row_layout.add_widget(name_label)
                    
                    # Round 3 score
                    score_color = POSITIVE if player['round_score'] >= 0 else NEGATIVE
                    round_score_label = Label(
                        text=f"R3: {player['round_score']:+.0f}",
                        color=score_color,
                        size_hint_x=0.2,
                        font_size='13sp'
                    )
                    row_layout.add_widget(round_score_label)
                    
                    # Final score
                    total_label = Label(
                        text=f"TOTAL: {player['total_score']:.0f}",
                        color=ACCENT_COLOR,
                        size_hint_x=0.3,
                        font_size='13sp',
                        bold=True
                    )
                    row_layout.add_widget(total_label)
                    
                    results_container.add_widget(row_layout)
                    
                    # Add separator
                    separator = Label(text='', size_hint_y=None, height=5)
                    results_container.add_widget(separator)
        
        except Exception as e:
            error_label = Label(text=f"Error loading scores: {str(e)}", color=NEGATIVE)
            results_container.add_widget(error_label)
        
        scroll.add_widget(results_container)
        layout.add_widget(scroll)
        
        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        end_btn = Button(
            text="View Final Results",
            background_color=POSITIVE,
            color=(1, 1, 1, 1)
        )
        end_btn.bind(on_press=self.end_game_actual)
        button_layout.add_widget(end_btn)
        
        back_btn = Button(
            text="Back to Scoring",
            background_color=NEGATIVE
        )
        back_btn.bind(on_press=lambda x: self.show_scoring_screen())
        button_layout.add_widget(back_btn)
        
        layout.add_widget(button_layout)
        self.root.add_widget(layout)
    
    def advance_to_next_round_actual(self, instance):
        """Actually advance to next round after showing summary."""
        try:
            response = requests.post(f"{BACKEND_URL}/game/{self.current_game['id']}/next-round")
            
            if response.status_code == 200:
                self.current_game = response.json()
                print(f"✓ Advanced to round {self.current_game['current_round']}")
                self.show_scoring_screen()
            else:
                self.show_popup('Error', f"Failed to advance: {response.text}")
        except Exception as e:
            self.show_popup('Error', f"Connection error: {str(e)}")
    
    def end_game_actual(self, instance):
        """Actually end the game after showing summary."""
        try:
            response = requests.post(f"{BACKEND_URL}/game/{self.current_game['id']}/complete")
            
            if response.status_code == 200:
                self.show_results_screen()
            else:
                self.show_popup('Error', f"Failed to end game: {response.text}")
        except Exception as e:
            self.show_popup('Error', f"Connection error: {str(e)}")
    
    def show_results_screen(self):
        """Display final results with round-by-round breakdown and export options."""
        self.root.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Title
        title = Label(
            text='[b][size=32]🏆 Game Results 🏆[/size][/b]',
            markup=True,
            color=ACCENT_COLOR,
            size_hint_y=0.08
        )
        layout.add_widget(title)
        
        # Refresh and show results
        self.refresh_game_state()
        sorted_players = sorted(self.players, key=lambda p: p['total_score'], reverse=True)
        
        # Add scroll view for results
        scroll = ScrollView(size_hint_y=0.6)
        results_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=10)
        results_container.bind(minimum_height=results_container.setter('height'))
        
        # Get round info
        rounds = self.current_game.get('rounds', [])
        
        # Show round-by-round breakdown
        for round_info in rounds:
            round_num = round_info['round_number']
            round_name = round_info['round_name']
            
            # Round header
            round_header = Label(
                text=f"[b]Round {round_num}: {round_name}[/b]",
                markup=True,
                color=ACCENT_COLOR,
                size_hint_y=None,
                height=35,
                font_size='13sp'
            )
            results_container.add_widget(round_header)
            
            # Scores for this round
            for player in sorted_players:
                # Calculate score for this round only
                round_score = 0
                for score in player.get('scores', []):
                    if score.get('round_number') == round_num:
                        round_score += score.get('points', 0)
                
                row = BoxLayout(orientation='horizontal', size_hint_y=None, height=30, spacing=10)
                
                name_label = Label(
                    text=f"  {player['name']}:",
                    color=TEXT_COLOR,
                    size_hint_x=0.6,
                    font_size='12sp'
                )
                row.add_widget(name_label)
                
                score_color = POSITIVE if round_score >= 0 else NEGATIVE
                score_label = Label(
                    text=f"{round_score:.0f}",
                    color=score_color,
                    size_hint_x=0.4,
                    font_size='12sp',
                    bold=True
                )
                row.add_widget(score_label)
                
                results_container.add_widget(row)
            
            # Divider
            divider = Label(text='', size_hint_y=None, height=5)
            results_container.add_widget(divider)
        
        # Overall totals
        total_header = Label(
            text="[b]FINAL SCORES[/b]",
            markup=True,
            color=ACCENT_COLOR,
            size_hint_y=None,
            height=35,
            font_size='14sp'
        )
        results_container.add_widget(total_header)
        
        for idx, player in enumerate(sorted_players, 1):
            medal = ['🥇', '🥈', '🥉'].get(idx - 1, '  ')
            
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
            
            medal_label = Label(text=medal, size_hint_x=0.1, font_size='20sp')
            row.add_widget(medal_label)
            
            name_label = Label(
                text=player['name'],
                color=TEXT_COLOR,
                size_hint_x=0.5,
                font_size='14sp',
                bold=True
            )
            row.add_widget(name_label)
            
            score_color = POSITIVE if player['total_score'] >= 0 else NEGATIVE
            score_label = Label(
                text=f"{player['total_score']:.0f}",
                color=score_color,
                size_hint_x=0.4,
                font_size='16sp',
                bold=True
            )
            row.add_widget(score_label)
            
            results_container.add_widget(row)
        
        scroll.add_widget(results_container)
        layout.add_widget(scroll)
        
        # Export and New Game buttons
        button_layout = BoxLayout(size_hint_y=0.25, spacing=15)
        
        export_btn = Button(text='📥 Export CSV', font_size='14sp', bold=True, background_color=ACCENT_COLOR)
        export_btn.bind(on_press=self.export_game_csv)
        button_layout.add_widget(export_btn)
        
        new_game_btn = Button(text='🎮 New Game', font_size='14sp', bold=True, background_color=POSITIVE)
        new_game_btn.bind(on_press=lambda x: self.show_player_entry_screen())
        button_layout.add_widget(new_game_btn)
        
        layout.add_widget(button_layout)
        
        self.root.add_widget(layout)
    
    def export_game_csv(self, instance):
        """Export game data as CSV."""
        try:
            response = requests.get(f"{BACKEND_URL}/game/{self.current_game['id']}/export/csv")
            
            if response.status_code == 200:
                data = response.json()
                
                # Save CSV file
                filename = f"game_{self.current_game['id']}.csv"
                filepath = os.path.expanduser(f"~/Downloads/{filename}")
                
                with open(filepath, 'w') as f:
                    f.write(data['content'])
                
                self.show_popup('Success', f"Game exported to:\n{filepath}")
            else:
                self.show_popup('Error', 'Failed to export game')
        except Exception as e:
            self.show_popup('Error', f"Export error: {str(e)}")
    
    def show_menu(self, instance):
        """Show menu with options."""
        pass  # Placeholder for menu functionality
    
    def show_load_games_screen(self, instance):
        """Show screen to load previous games."""
        pass  # Placeholder for loading previous games
    
    def show_popup(self, title, message):
        """Show a popup dialog."""
        popup = Popup(
            title=title,
            size_hint=(0.9, 0.4),
            background_color=DARK_BG
        )
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        msg_label = Label(text=message, color=TEXT_COLOR, size_hint_y=0.7)
        layout.add_widget(msg_label)
        
        close_btn = Button(text='OK', size_hint_y=0.3, background_color=ACCENT_COLOR)
        close_btn.bind(on_press=popup.dismiss)
        layout.add_widget(close_btn)
        
        popup.content = layout
        popup.open()


if __name__ == '__main__':
    app = NationWantsToGuessApp()
    app.run()
