# About GameRoom

The Card Game is a two-player turn-based game where players compete to earn the highest score by choosing cards from their hand. The game utilizes the Pygame library for graphics and networking capabilities to communicate with a server.

Upon starting the game, players are prompted to log in with their credentials. Once logged in, the game establishes a connection with the server. The server then assigns opponents and provides the players with their initial card decks.

The game window displays the player's hand of cards. Players can click on a card to select it. Once a card is chosen, it is sent to the server for processing. The server determines the outcome of the card selection and updates the players' scores accordingly. The chosen card is removed from the player's hand, and the turn is passed to the opponent.

The game continues until one of the players runs out of cards in their hand, indicating the end of the match. At this point, the winner is determined based on the players' scores. The game displays the winner's name on the screen.

Additionally, the game includes integration with a Django server to handle authentication and store player scores. The game communicates with the server to authenticate the players and send/receive scores.

Please note that the provided code is incomplete and includes placeholders for additional functionality, such as creating match rooms and sending player scores to the server.