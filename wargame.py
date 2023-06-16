import pygame
import random
import socket

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("War Card Game")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up fonts
font = pygame.font.Font(None, 36)

# Load card images
card_images = {}
suits = ['hearts', 'diamonds', 'clubs', 'spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

for suit in suits:
    for rank in ranks:
        card_name = f"{rank}_of_{suit}"
        card_images[card_name] = pygame.image.load(f"cards/{card_name}.png")

# Create deck and shuffle it
deck = list(card_images.keys())
random.shuffle(deck)

# Divide the deck between players
player1_deck = deck[:25]
player2_deck = deck[25:]

# Set up game variables
player1_score = 0
player2_score = 0
game_over = False

# # Set up networking
# HOST = "127.0.0.1"  # Replace with your server IP
# PORT = 5555  # Replace with your desired port number

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((HOST, PORT))


# def send_data(data):
#     message = str.encode(data)
#     client_socket.sendall(message)


# def receive_data():
#     data = client_socket.recv(1024).decode()
#     return data


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Check for key press
            if len(player1_deck) > 0 and len(player2_deck) > 0:
                player1_card = player1_deck.pop(0)
                player2_card = player2_deck.pop(0)

                screen.fill(BLACK)
                # Draw player scores
                player1_text = font.render(f"Player 1 Score: {player1_score}", True, WHITE)
                player2_text = font.render(f"Player 2 Score: {player2_score}", True, WHITE)
                screen.blit(player1_text, (50, 50))
                screen.blit(player2_text, (50, 100))

                screen.blit(card_images[player1_card], (250, 250))
                screen.blit(card_images[player2_card], (450, 250))

                if ranks.index(player1_card.split('_')[0]) > ranks.index(player2_card.split('_')[0]):
                    player1_score += 2
                elif ranks.index(player2_card.split('_')[0]) > ranks.index(player1_card.split('_')[0]):
                    player2_score += 2
                else:
                    player1_deck.append(player1_card)
                    player2_deck.append(player2_card)

                pygame.display.flip()

                # # Send game state to the server
                # game_state = f"{player1_score}:{player2_score}:{len(player1_deck)}:{len(player2_deck)}"
                # send_data(game_state)

                # # Receive game state from the server
                # opponent_state = receive_data()
                # print("Opponent State:", opponent_state)
                # opponent_score, opponent_deck_size = map(int, opponent_state.split(':'))

                # # Update opponent's score and deck size
                # player2_score = opponent_score
                # player2_deck = deck[-opponent_deck_size:]

            # Check for game over condition
            if len(player1_deck) == 0 or len(player2_deck) == 0:
                game_over = True

# Show the winner
if player1_score > player2_score:
    winner_text = font.render("Player 1 wins!", True, BLACK)
else:
    winner_text = font.render("Player 2 wins!", True, BLACK)

screen.blit(
    winner_text,
    (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2),
)
pygame.display.flip()

# Wait for the user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
