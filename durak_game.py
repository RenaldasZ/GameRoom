import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Durak Card Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define card dimensions
CARD_WIDTH = 21
CARD_HEIGHT = 36

# Define the table position
TABLE_X = 50
TABLE_Y = screen_height // 2 - CARD_HEIGHT // 2

# Define the player positions
PLAYER_POSITIONS = [
    (TABLE_X, TABLE_Y + CARD_HEIGHT + 20),
    (TABLE_X + CARD_WIDTH + 20, TABLE_Y),
    (TABLE_X + 3 * CARD_WIDTH + 40, TABLE_Y),
    (TABLE_X + 4 * CARD_WIDTH + 60, TABLE_Y + CARD_HEIGHT + 20),
    (TABLE_X + 2 * CARD_WIDTH + 40, TABLE_Y + 2 * (CARD_HEIGHT + 20))
]

# Define card images
card_images = {}

# Load card images
def load_card_images():
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

    for suit in suits:
        for rank in ranks:
            filename = f'cards/{rank}_of_{suit}.png'
            image = pygame.image.load(filename)
            card_images[(suit, rank)] = image

# Call the function to load the card images
load_card_images()

# Create a deck of cards
suits = ['hearts', 'diamonds', 'clubs', 'spades']
ranks = ['6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

deck = []

for suit in suits:
    for rank in ranks:
        card = {
            'suit': suit,
            'rank': rank,
            'image': card_images[(suit, rank)]  # Load card image based on suit and rank
        }
        deck.append(card)

# Shuffle the deck
random.shuffle(deck)

# Deal cards to players
num_players = 4
cards_per_player = 6

players = [[] for _ in range(num_players)]  # Create an empty list for each player's hand

for _ in range(cards_per_player):
    for player in players:
        card = deck.pop(0)  # Remove the first card from the deck and assign it to the player
        player.append(card)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw the table
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (TABLE_X, TABLE_Y, 5 * CARD_WIDTH + 60, CARD_HEIGHT + 20), 2)

    # Draw player hands
    # for i, player_position in enumerate(PLAYER_POSITIONS):
    #     player_hand = players[i]  # Get the current player's hand
    #     x, y = player_position  # Get the position of the player's hand on the screen

    #     for card in player_hand:
    #         image = card['image']
    #         screen.blit(image, (x, y))
    #         x += CARD_WIDTH + 20  # Adjust the x-coordinate for the next card

    pygame.display.flip()
