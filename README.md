# IFP_Sum2_project
Repository for Sam, Salavat, Majed, and Pratish Summative 2 python card game

## Football Card Game

A card game where two players compete in a football-themed match using cards with different values.

### Game Rules

1. The deck of cards is divided into two players.
2. Each player draws four cards from the top of their deck to form their team:
   - Three defenders
   - One goalkeeper
3. The player who moves first becomes the attacker and takes cards from the top of their deck to attack.
4. The attacker must beat all three defender cards, and then the goalkeeper's card to score a goal.
5. A card is beaten if:
   - The attacking card's face value is higher than the defense card
   - OR if the defense card has the maximum face value (10) and the attack card has the minimum face value (1)
6. All beaten cards are placed at the bottom of the attacking player's deck.
7. If an attack card cannot beat a defense card, both cards go to the defending player's deck and the turn switches.
8. If the attacking player runs out of cards in their deck, they must use their defense cards to continue attacking.

### Controls

- **SPACE**: Draw an attack card and process the attack
- **R**: Reset the game
- **ESC**: Quit the game

### Installation

1. Make sure you have Python 3.6+ installed
2. Install requirements:
   ```
   pip install -r requirements.txt
   ```
3. Run the game:
   ```
   python prototype.py
   ```
