import http.client
from sys import argv
import json
import re

def create_connection(port=8080, host=''):
    conn = http.client.HTTPConnection(host, port)
    conn.request("GET", "/list")
    response = conn.getresponse()
    string = response.read().decode('utf-8')
    json_data = json.loads(string)
    for game in json_data:
        print(str(game['id']) + ' ' + game['name'])
    command = input('Type id number to join a game or type new to start a new game:')
    if command.startswith('new'):
        name_regex = re.compile(r"new (.*)")
        is_name = name_regex.match(command)
        if is_name:
            conn.request("GET", "/start?name=" + is_name.group(1))
        else:
            conn.request("GET", "/start?name=")
        response = conn.getresponse()
        string = response.read().decode('utf-8')
        json_data = json.loads(string)
        play(json_data['id'], 1, conn)
    else:
        play(command, 2, conn)
    conn.close()

def play(game, player_number, conn):
    check_game(game, player_number, conn)
    running = True
    while running:
        take_turn(player_number, game, conn)
        running = check_game(game, player_number, conn)

def take_turn(player_number, game, conn):
    playing = True
    mark = 'x' if player_number == 1 else 'o'
    while playing:
        command = input('your turn ('+ mark +'):')
        if len(command) != 3:
            print("invalid input")
            continue
        conn.request("GET", "/play?game=" + str(game) + "&player=" + str(player_number) + "&x=" + command[0] + "&y=" + command[2])
        response = conn.getresponse()
        if response.status == 404:
            print("invalid input")
            continue
        string = response.read().decode('utf-8')
        json_data = json.loads(string)
        if json_data['status'] == 'bad':
            print(json_data['message'])
            continue
        playing = False


def check_game(game, player_number, conn):
    conn.request("GET", "/status?game=" + str(game))
    response = conn.getresponse()
    if response.status == 404:
        return True
    string = response.read().decode('utf-8')
    json_data = json.loads(string)
    if 'winner' in json_data:
        if json_data['winner'] == player_number:
            print('you win')
        elif json_data['winner'] == 0:
            print('draw')
        else:
            print('you lose')
        return False
    print_board(json_data['board'])
    return True

def print_board(board):
    for line in board:
        for column in line:
            if column == 1:
                print('x', end='', flush=True)
            elif column == 2:
                print('o', end='', flush=True)
            else:
                print('_', end='', flush=True)
        print()

if __name__ == '__main__':
    try:
        port = int(argv[2])
        host = argv[1]
        if port < 1:
            print("Third parameter has to be larger than zero")
        elif port > 65535:
            print("Third parameter has to be less than 65536")
        else:
            create_connection(port=port, host=host)
    except ValueError:
        print("Third parameter has to be integer")
