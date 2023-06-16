import socket

HOST = "127.0.0.1"  # Replace with your server IP
PORT = 5555  # Replace with your desired port number

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"Server listening on {HOST}:{PORT}")

client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

# Set up initial game state
player1_score = 0
player1_deck_size = 25

while True:
    data = client_socket.recv(1024).decode()
    if not data:
        break
    print(f"Received data from client: {data}")

    # Process the data and update the game state
    opponent_score, opponent_deck_size = map(int, data.split(':'))

    # Update player1's score and deck size based on the opponent's state
    player1_score = opponent_score
    player1_deck_size = opponent_deck_size

    # Determine player2's state (opponent's state)
    # Implement your game logic and update player2's score and deck size accordingly
    player2_score = 0
    player2_deck_size = 25

    # Send the opponent's game state back to the client
    opponent_state = f"{player2_score}:{player2_deck_size}"
    client_socket.sendall(str.encode(opponent_state))

client_socket.close()
server_socket.close()
