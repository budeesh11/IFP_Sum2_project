from game_engine import GameEngine

class GameCLI:
    def __init__(self, engine: GameEngine):
        self.engine = engine
        
    def display_game_state(self):
        player = self.engine.attacker if self.engine.attacker.name == "Player" else self.engine.defender
        computer = self.engine.defender if self.engine.attacker.name == "Player" else self.engine.attacker
        
        print(f"{self.engine.attacker.name}'s Turn. Goals: {player.goals}:{computer.goals}")
        print()
        print("Computer Active Cards:", computer.display_active_cards())
        print("Attack Card:", self.engine.attack_card.display() if self.engine.attack_card else "None")
        print("Player Active Cards:", player.display_active_cards())
        print()