# GameRoom Overview

**The Card Game** is a two-player turn-based game where players compete to earn the highest score by choosing cards from their hand. The game utilizes the Pygame library for graphics and networking capabilities to communicate with a server.

## Game Flow

1. **Login**: Upon starting the game, players are prompted to log in with their credentials. 

2. **Server Connection**: Once logged in, the game establishes a connection with the server. The server assigns opponents and provides the players with their initial card decks.

3. **Player's Hand**: The game window displays the player's hand of cards. Players can click on a card to select it. 

4. **Card Processing**: Once a card is chosen, it is sent to the server for processing. The server determines the outcome of the card selection and updates the players' scores accordingly. The chosen card is removed from the player's hand, and the turn is passed to the opponent.

5. **End of Match**: The game continues until one of the players runs out of cards in their hand, indicating the end of the match. 

6. **Determining the Winner**: At this point, the winner is determined based on the players' scores. The game displays the winner's name on the screen.

## Integration with Django Server

The game includes integration with a Django server to handle authentication and store player scores. The game communicates with the server to authenticate the players and send/receive scores.

## Note

Please note that the provided code is incomplete and includes placeholders for additional functionality, such as creating match rooms and sending player scores to the server.

