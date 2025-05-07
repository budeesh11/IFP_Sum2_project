from game_engine import GameEngine

class GameCLI:
    def __init__(self, engine: GameEngine):
        self.engine = engine
        
    def display_game_state(self):
        player = self.engine.attacker if self.engine.attacker.name == "Player" else self.engine.defender
        computer = self.engine.defender if self.engine.attacker.name == "Player" else self.engine.attacker
        
        print("===========================================")
        print(f"{self.engine.attacker.name}'s Turn. Goals: {player.goals}:{computer.goals}")
        print()
        print("Total cards in game: " + str(len(computer.deck) + len(player.deck) + len(computer.active_cards) + len(player.active_cards) + 1 if self.engine.attack_card else 0))
        print("Computer deck: " + str(len(computer.deck)))
        print("Computer Active Cards:", computer.display_active_cards())
        print("Attack Card:", self.engine.attack_card.display() if self.engine.attack_card else "None")
        print("Player Active Cards:", player.display_active_cards())
        print("Player deck: " + str(len(player.deck)))
        print()
        print("Battle cards: " + self.display_battle_cards())
        print()
        print("===========================================")
    
    def display_battle_cards(self):
        result = ""
        for card in self.engine.battle_cards:
            result += card.display() + " "
        return result