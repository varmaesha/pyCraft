"""
Simple table-based UI for Nation Wants to Guess scoring app.
Click cells to update scores, simple interface with no fancy styling.

App flow:
1. show_player_entry: enter 3 player names.
2. start_game: send names to backend and receive game state.
3. show_scoring_table: display current round, per-player scores, and totals.
4. edit_score: add or edit scores for a player and round.
5. next_round: advance the game to the next round.
6. end_game: complete the game after all rounds and show final results.
7. export_csv: save a CSV export of the current game.
"""
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
import requests
from datetime import datetime

Window.size = (900, 600)

BACKEND_URL = "http://127.0.0.1:8001"


class ScoringApp(App):
    """Main scoring app for Nation Wants to Guess."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_game = None
        self.players = []
        self.selected_cell = None
    
    def build(self):
        """Build the root widget and start with the player entry screen."""
        self.title = "Nation Wants to Guess - Scoring"
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.show_player_entry()
        return self.root
    
    def on_start(self):
        """Verify backend connectivity when the app starts."""
        try:
            response = requests.get(f"{BACKEND_URL}/", timeout=2)
            print(f"✓ Backend connected")
        except:
            print(f"✗ Backend not running at {BACKEND_URL}")
    
    def show_player_entry(self):
        """Simple screen to enter 3 player names."""
        self.root.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title = Label(text="Enter 3 Player Names:", size_hint_y=0.2, font_size='20sp')
        layout.add_widget(title)
        
        # Input fields
        inputs_layout = GridLayout(cols=1, spacing=10, size_hint_y=0.5)
        
        self.name_inputs = []
        for i in range(3):
            name_input = TextInput(
                text=f'Player {i+1}',
                multiline=False,
                size_hint_y=None,
                height=40
            )
            inputs_layout.add_widget(name_input)
            self.name_inputs.append(name_input)
        
        layout.add_widget(inputs_layout)
        
        # Start button
        start_btn = Button(text='START GAME', size_hint_y=0.2)
        start_btn.bind(on_press=self.start_game)
        layout.add_widget(start_btn)
        
        self.root.add_widget(layout)
    
    def start_game(self, instance):
        """Start game with entered player names."""
        names = [inp.text.strip() or f'Player {i+1}' for i, inp in enumerate(self.name_inputs)]
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/game/start",
                json={"player_names": names}
            )
            if response.status_code == 200:
                self.current_game = response.json()
                print(f"✓ Game started with ID: {self.current_game['id']}")
                self.refresh_game()
                self.show_scoring_table()
            else:
                self.show_popup("Error", "Failed to start game")
        except Exception as e:
            self.show_popup("Error", f"Connection error: {str(e)}")
    
    def refresh_game(self):
        """Fetch latest game state."""
        try:
            response = requests.get(f"{BACKEND_URL}/game/{self.current_game['id']}")
            if response.status_code == 200:
                self.current_game = response.json()
                self.players = self.current_game.get('players', [])
                print(f"✓ Game refreshed")
        except Exception as e:
            print(f"✗ Refresh error: {e}")
    
    def show_scoring_table(self):
        """Display simple scoring table."""
        self.root.clear_widgets()
        self.refresh_game()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title with round info
        current_round = self.current_game.get('current_round', 1)
        round_name = ""
        for r in self.current_game.get('rounds', []):
            if r['round_number'] == current_round:
                round_name = r['round_name']
                break
        
        title = Label(
            text=f"Round {current_round}: {round_name}",
            size_hint_y=0.08,
            font_size='18sp',
            bold=True
        )
        layout.add_widget(title)
        
        # Scoring table
        scroll = ScrollView(size_hint_y=0.75)
        table = GridLayout(cols=5, spacing=5, size_hint_y=None, padding=5)
        table.bind(minimum_height=table.setter('height'))
        
        # Header row
        headers = ['Player', 'R1', 'R2', 'R3', 'Total']
        for header in headers:
            lbl = Label(text=header, bold=True, size_hint_y=None, height=40)
            table.add_widget(lbl)
        
        # Calculate round scores
        scores_by_round = {}
        for score_entry in self.current_game.get('scores', []):
            round_num = score_entry.get('round_number')
            player_id = score_entry.get('player_id')
            points = score_entry.get('points', 0)
            
            if round_num not in scores_by_round:
                scores_by_round[round_num] = {}
            
            if player_id not in scores_by_round[round_num]:
                scores_by_round[round_num][player_id] = 0
            
            scores_by_round[round_num][player_id] += points
        
        # Data rows
        for player in self.players:
            pid = player['id']
            
            # Player name
            name_label = Label(text=player['name'], size_hint_y=None, height=40)
            table.add_widget(name_label)
            
            # Scores for each round
            for round_num in [1, 2, 3]:
                score = scores_by_round.get(round_num, {}).get(pid, 0)
                btn = Button(
                    text=str(int(score)),
                    size_hint_y=None,
                    height=40,
                    background_color=(0.2, 0.2, 0.2, 1)
                )
                btn.bind(on_press=lambda b, p=pid, r=round_num: self.edit_score(p, r))
                table.add_widget(btn)
            
            # Total
            total_label = Label(
                text=str(int(player['total_score'])),
                size_hint_y=None,
                height=40,
                bold=True
            )
            table.add_widget(total_label)
        
        scroll.add_widget(table)
        layout.add_widget(scroll)
        
        # Control buttons
        btn_layout = GridLayout(cols=4, spacing=10, size_hint_y=0.12)
        
        next_round_btn = Button(text=f'Next Round →' if current_round < 3 else 'Final Round')
        next_round_btn.bind(on_press=self.next_round)
        btn_layout.add_widget(next_round_btn)
        
        end_game_btn = Button(text='End Game')
        end_game_btn.bind(on_press=self.end_game)
        btn_layout.add_widget(end_game_btn)
        
        export_btn = Button(text='Export CSV')
        export_btn.bind(on_press=self.export_csv)
        btn_layout.add_widget(export_btn)
        
        refresh_btn = Button(text='Refresh')
        refresh_btn.bind(on_press=lambda x: self.show_scoring_table())
        btn_layout.add_widget(refresh_btn)
        
        layout.add_widget(btn_layout)
        self.root.add_widget(layout)
    
    def edit_score(self, player_id, round_num):
        """Pop up to edit score for a cell with quick buttons."""
        popup = Popup(
            title=f'Edit Score - Round {round_num}',
            size_hint=(0.7, 0.5)
        )
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Custom input field
        input_field = TextInput(
            text='',
            multiline=False,
            size_hint_y=0.2,
            input_filter='float'
        )
        content.add_widget(input_field)
        
        # Quick buttons layout
        quick_btns = BoxLayout(size_hint_y=0.3, spacing=10)
        
        def add_score_value(points):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/game/{self.current_game['id']}/score",
                    json={
                        "player_id": player_id,
                        "points": points,
                        "round_number": round_num
                    }
                )
                if response.status_code == 200:
                    popup.dismiss()
                    self.show_scoring_table()
                else:
                    self.show_popup("Error", "Failed to add score")
            except Exception as e:
                self.show_popup("Error", f"Error: {str(e)}")
        
        # +10 button
        btn_10 = Button(text='+10')
        btn_10.bind(on_press=lambda x: add_score_value(10))
        quick_btns.add_widget(btn_10)
        
        # +20 button
        btn_20 = Button(text='+20')
        btn_20.bind(on_press=lambda x: add_score_value(20))
        quick_btns.add_widget(btn_20)
        
        # Custom button
        btn_custom = Button(text='Custom')
        def add_custom(instance):
            try:
                points = float(input_field.text) if input_field.text else 0
                add_score_value(points)
            except:
                self.show_popup("Error", "Invalid number")
        btn_custom.bind(on_press=add_custom)
        quick_btns.add_widget(btn_custom)
        
        content.add_widget(quick_btns)
        
        # Bottom buttons
        btn_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        
        ok_btn = Button(text='Add')
        ok_btn.bind(on_press=lambda x: add_score_value(float(input_field.text) if input_field.text else 0))
        btn_layout.add_widget(ok_btn)
        
        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=popup.dismiss)
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(btn_layout)
        popup.content = content
        popup.open()
    
    def next_round(self, instance):
        """Advance to next round."""
        try:
            response = requests.post(f"{BACKEND_URL}/game/{self.current_game['id']}/next-round")
            if response.status_code == 200:
                self.show_scoring_table()
            else:
                self.show_popup("Error", "Failed to advance round")
        except Exception as e:
            self.show_popup("Error", f"Error: {str(e)}")
    
    def end_game(self, instance):
        """End game and show results."""
        current_round = self.current_game.get('current_round', 1)
        if current_round < 3:
            self.show_popup("Info", "Game must complete all 3 rounds first")
            return
        
        try:
            response = requests.post(f"{BACKEND_URL}/game/{self.current_game['id']}/complete")
            if response.status_code == 200:
                self.show_results()
            else:
                self.show_popup("Error", "Failed to end game")
        except Exception as e:
            self.show_popup("Error", f"Error: {str(e)}")
    
    def show_results(self):
        """Display final results."""
        self.root.clear_widgets()
        self.refresh_game()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title = Label(text="FINAL RESULTS", size_hint_y=0.1, font_size='24sp', bold=True)
        layout.add_widget(title)
        
        # Results table
        scroll = ScrollView(size_hint_y=0.7)
        table = GridLayout(cols=3, spacing=5, size_hint_y=None, padding=5)
        table.bind(minimum_height=table.setter('height'))
        
        # Header
        for header in ['Rank', 'Player', 'Score']:
            lbl = Label(text=header, bold=True, size_hint_y=None, height=40)
            table.add_widget(lbl)
        
        # Sort by total score
        sorted_players = sorted(self.players, key=lambda p: p['total_score'], reverse=True)
        
        medals = ['🥇', '🥈', '🥉']
        for idx, player in enumerate(sorted_players):
            medal = medals[idx] if idx < 3 else f"{idx+1}."
            table.add_widget(Label(text=medal, size_hint_y=None, height=40))
            table.add_widget(Label(text=player['name'], size_hint_y=None, height=40))
            table.add_widget(Label(text=str(int(player['total_score'])), size_hint_y=None, height=40))
        
        scroll.add_widget(table)
        layout.add_widget(scroll)
        
        # Buttons
        btn_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.15)
        
        export_btn = Button(text='Export CSV')
        export_btn.bind(on_press=self.export_csv)
        btn_layout.add_widget(export_btn)
        
        new_game_btn = Button(text='New Game')
        new_game_btn.bind(on_press=lambda x: self.show_player_entry())
        btn_layout.add_widget(new_game_btn)
        
        layout.add_widget(btn_layout)
        self.root.add_widget(layout)
    
    def export_csv(self, instance):
        """Export game to CSV."""
        try:
            response = requests.get(f"{BACKEND_URL}/game/{self.current_game['id']}/export/csv")
            if response.status_code == 200:
                data = response.json()
                filename = f"game_{self.current_game['id']}.csv"
                filepath = os.path.expanduser(f"~/Downloads/{filename}")
                
                with open(filepath, 'w') as f:
                    f.write(data['content'])
                
                self.show_popup('Success', f"Exported to:\n{filepath}")
            else:
                self.show_popup('Error', 'Failed to export')
        except Exception as e:
            self.show_popup('Error', f"Export error: {str(e)}")
    
    def show_popup(self, title, message):
        """Show simple popup."""
        popup = Popup(title=title, size_hint=(0.9, 0.4))
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text=message))
        close_btn = Button(text='OK', size_hint_y=0.3)
        close_btn.bind(on_press=popup.dismiss)
        layout.add_widget(close_btn)
        popup.content = layout
        popup.open()


if __name__ == '__main__':
    app = ScoringApp()
    app.run()
