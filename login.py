import pygame
from pygame.locals import *

class LoginScreen:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Login Screen')
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.font = pygame.font.Font(None, 32)
        self.username = ''
        self.password = ''

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    if self.is_username_active():
                        self.username = self.username[:-1]
                    elif self.is_password_active():
                        self.password = self.password[:-1]
                elif event.key == K_TAB:
                    self.toggle_username_active()
                    self.toggle_password_active()
                elif event.key == K_RETURN:
                    if self.username and self.password:
                        return True
                else:
                    if self.is_username_active():
                        self.username += event.unicode
                    elif self.is_password_active():
                        self.password += event.unicode

        return None

    def display(self):
        self.screen.fill(self.WHITE)
        title_text = self.font.render('Login', True, self.BLACK)
        username_text = self.font.render('Username:', True, self.BLACK)
        password_text = self.font.render('Password:', True, self.BLACK)
        username_input = self.font.render(self.username, True, self.BLACK)
        password_input = self.font.render('*' * len(self.password), True, self.BLACK)
        username_rect = pygame.Rect(200, 200, 400, 50)
        password_rect = pygame.Rect(200, 300, 400, 50)
        pygame.draw.rect(self.screen, self.BLACK, username_rect, 2)
        pygame.draw.rect(self.screen, self.BLACK, password_rect, 2)
        self.screen.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))
        self.screen.blit(username_text, (100, 200))
        self.screen.blit(password_text, (100, 300))
        self.screen.blit(username_input, (210, 210))
        self.screen.blit(password_input, (210, 310))
        pygame.display.flip()

    def is_username_active(self):
        return self.username_active

    def is_password_active(self):
        return self.password_active

    def toggle_username_active(self):
        self.username_active = not self.is_username_active()

    def toggle_password_active(self):
        self.password_active = not self.is_password_active()

    def run(self):
        self.username_active = True
        self.password_active = False

        while True:
            result = self.handle_events()
            if result is not None:
                return result
            self.display()

class CardGame:
    def __init__(self):
        self.login_screen = LoginScreen()

    def run(self):
        while True:
            if self.login_screen.run():
                break

        # Get user login credentials from the login screen
        username = self.login_screen.username
        password = self.login_screen.password

        # ... (the rest of your code)

game = CardGame()
game.run()
