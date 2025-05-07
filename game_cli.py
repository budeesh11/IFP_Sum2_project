from game_engine import gameEngine

class gameCLI:
    def __init__(self, engine: gameEngine):
        self.engine = engine
        
    def print_game_state(self):
        print(f"{self.engine.attacker.name}'s Turn. Goals: {self.engine.attacker.goals}")
        print("Attack Card:", self.engine.attack_card)
        print("Defender Active Cards:", self.engine.defender.active_cards)