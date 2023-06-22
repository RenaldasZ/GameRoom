# wargame.py
import pygame
import socket
import pickle
from card import Card
import http.client
import json
from login import LoginScreen


class CardGame:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Set up the game window
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Card Game')

        # load bg image and change scale
        self.background = pygame.image.load('cards/game_bg.jpg')
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

        # Set up card dimensions
        self.card_width, self.card_height = 180, int(180 * 140 / 100)

        # Set up colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.CARD_IMAGE_WIDTH = 180
        self.font = pygame.font.Font(None, 30)

        # Create a login screen and run it
        self.login_screen = LoginScreen()
        self.login_screen.run()

        # Get user login credentials from the login screen
        self.username = self.login_screen.username
        self.password = self.login_screen.password

        # Flag to indicate if the game is over
        self.game_over = False

        # Connect to django and game server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('127.0.0.1', 5000)
        self.django_server = http.client.HTTPConnection("127.0.0.1", 8000)
        self.headers = {
        "Accept": "*/*",
        "User-Agent": "War game client",
        "Content-Type": "application/json" 
        }
        payload = json.dumps({
        "username": self.username,
        "password": self.password
        })
        try:
            self.django_server.request("POST", "/api-token-auth/", payload, self.headers)
            response = self.django_server.getresponse()
        except Exception as e:
            print(e)
        else:
            result = json.loads(response.read())
            print(result['token'])
            self.score_server_token = result['token']

        #Connect to game server
        try:
            self.client_socket.connect(self.server_address)
            print('Connected to:', self.server_address)
        except ConnectionRefusedError:
            print('Failed to connect to the server. Please make sure the server is running.')
            pygame.quit()
            return
        
        #Send self username and receive opponent username and own card deck
        try:
            self.client_socket.sendall(pickle.dumps(self.username))
            self.opponent_username = pickle.loads(self.client_socket.recv(1024))
            self.player_hand = pickle.loads(self.client_socket.recv(1024))
        except (pickle.PicklingError, pickle.UnpicklingError, socket.error) as e:
            print('Failed to initialize the game:', e)
            self.client_socket.close()
            pygame.quit()
            return

        # Initialize player scores
        self.player1_score = 0
        self.player2_score = 0   

        # Load card images
        self.card_images = {}
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

        for suit in suits:
            for rank in ranks:
                card_name = f"{rank}_of_{suit}"
                card_image_path = f"cards/{card_name}.png"
                card_image = pygame.image.load(card_image_path)
                card_image = pygame.transform.scale(card_image, (self.CARD_IMAGE_WIDTH, int(self.CARD_IMAGE_WIDTH * card_image.get_height() / card_image.get_width())))
                self.card_images[card_name] = card_image

    def opponents_turn(self):
        title_text = self.font.render(f"{self.opponent_username} Turn!", True, self.WHITE)
        title2_text = self.font.render(f"please wait for your turn.", True, self.WHITE)
        self.screen.blit(title_text, (self.screen_width / 2 - 60, 100))
        self.screen.blit(title2_text, (self.screen_width / 2 - 120, 120))
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_button_down(event)

    def handle_mouse_button_down(self, event):
        if event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            chosen_card = self.check_clicked_card(mouse_x, mouse_y)
            if chosen_card is not None:
                self.process_chosen_card(chosen_card)

    def check_clicked_card(self, mouse_x, mouse_y):
        for i, card in enumerate(self.player_hand[:4]):
            x = 100 + i * (self.card_width - 40)
            y = self.screen_height - self.card_height - 100

            if x <= mouse_x <= x + self.card_width and y <= mouse_y <= y + self.card_height:
                return self.player_hand[i]

        return None
    
    def process_chosen_card(self, chosen_card):
        print("Player chose:", chosen_card)
        self.opponents_turn()

        # Serialize and send the chosen card to the server
        try:
            serialized_card = pickle.dumps(chosen_card)
            self.client_socket.sendall(serialized_card)
        except (pickle.PickleError, socket.error):
            print('Failed to send the chosen card to the server.')
            self.client_socket.close()
            pygame.quit()
            return

        # Receive the result and scores from the server
        try:
            result, player1_score, player2_score = pickle.loads(self.client_socket.recv(1024))
            self.player1_score = player1_score
            self.player2_score = player2_score
        except pickle.UnpicklingError:
            print('Failed to receive the result and scores from the server.')
            self.client_socket.close()
            pygame.quit()
            return

        # Remove the chosen card from the player's hand
        self.player_hand.remove(chosen_card)

        # Check if the player's hand is empty
        if len(self.player_hand) == 0:
            self.game_over = True
            print("Match is over!")

            self.send_player_score_to_server()

    def winner_display(self):
        if self.player1_score > self.player2_score:
            font = pygame.font.Font(None, 40)
            game_winner = font.render(f"Winner {self.username}", True, self.WHITE)
            self.screen.blit(game_winner, (300, 200))
            print("Winner")
        elif self.player1_score < self.player2_score:
            font = pygame.font.Font(None, 40)
            game_loser = font.render(f"Loser! {self.username}", True, self.WHITE)
            self.screen.blit(game_loser, (300, 200))
            print("Loser")
        else:
            font = pygame.font.Font(None, 40)
            game_tie = font.render(f"Tie! That\'s a miracle!", True, self.WHITE)
            self.screen.blit(game_tie, (200, 200))
            print("Tie! That\'s a miracle!")

    def send_player_score_to_server(self):
        self.django_server = http.client.HTTPConnection("127.0.0.1", 8000)
        self.headers = {
            "Accept": "*/*",
            "User-Agent": "war game client",
            "Authorization": "Token " + self.score_server_token,
            "Content-Type": "application/json"
        }
        payload = json.dumps({
            "score": self.player1_score
        })
        self.django_server.request("POST", "/player/", payload, self.headers)
        response = self.django_server.getresponse()
        result = response.read()

    def display_cards(self):
        self.screen.blit(self.background, (0, 0))
        # Display the player's hand
        for i, card in enumerate(self.player_hand[:4]):
            x = 100 + i * (self.card_width - 40)
            y = self.screen_height - self.card_height - 100
            pygame.draw.rect(self.screen, self.BLACK, (x, y, self.card_width, self.card_height))
            pygame.draw.rect(self.screen, self.WHITE, (x, y, self.card_width, self.card_height))
            card_name = f"{card.rank}_of_{card.suit}".lower()
            card_image = self.card_images.get(card_name)
            if card_image:
                card_image = pygame.transform.scale(card_image, (self.card_width, self.card_height))  # Resize the card image
                self.screen.blit(card_image, (x, y))

        # Display player scores
        font = pygame.font.Font(None, 30)
        player1_score_text = font.render(f"{self.username}: " + str(self.player1_score), True, self.WHITE)
        player2_score_text = font.render(f"{self.opponent_username}: " + str(self.player2_score), True, self.WHITE)
        self.screen.blit(player1_score_text, (20, 20))
        self.screen.blit(player2_score_text, (20, 60))

        if self.game_over == True:  
            self.winner_display()
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.display_cards()

        self.client_socket.close()
        pygame.quit()

if __name__ == '__main__':
    game = CardGame()
    game.run()
