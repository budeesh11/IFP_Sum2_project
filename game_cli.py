from game_engine import GameEngine
import time

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
    
    def display_draw_situation(self):
        player = self.engine.attacker if self.engine.attacker.name == "Player" else self.engine.defender
        computer = self.engine.defender if self.engine.attacker.name == "Player" else self.engine.attacker
        draw_series_length = len(self.engine.draw_pile) // 2
        print("===========================================")
        print(f"{self.engine.attacker.name}'s Turn. Goals: {player.goals}:{computer.goals}")
        print("DRAW")
        for i in range(draw_series_length):
            print("  Attacker:", self.engine.draw_pile[i*2].display())
            print("  Defender:", self.engine.draw_pile[i*2+1].display())
            print()
        print("===========================================")
        time.sleep(1)
    
    def display_winning(self):
        player = self.engine.attacker if self.engine.attacker.name == "Player" else self.engine.defender
        computer = self.engine.defender if self.engine.attacker.name == "Player" else self.engine.attacker
        if self.engine.attacker.goals == 3:
            print("===========================================")
            print(self.engine.attacker.name + " wins!")
            print(f"Goals: {player.goals}:{computer.goals}")
            print("===========================================")
        elif self.engine.defender.goals == 3:
            print("===========================================")
            print(self.engine.defender.name + " wins!")
            print(f"Goals: {player.goals}:{computer.goals}")
            print("===========================================")
        elif len(self.engine.attacker.deck) == 0 and len(self.engine.attacker.active_cards) == 0:
            print("===========================================")
            print(self.engine.defender.name + " wins by default!")
            print(f"{self.engine.attacker.name} ran out of cards.")
            print(f"Goals: {player.goals}:{computer.goals}")
            print("===========================================")
        elif len(self.engine.defender.deck) == 0 and len(self.engine.defender.active_cards) == 0:
            print("===========================================")
            print(self.engine.attacker.name + " wins by default!")
            print(f"{self.engine.defender.name} ran out of cards.")
            print(f"Goals: {player.goals}:{computer.goals}")
            print("===========================================")
        
        
        
            
