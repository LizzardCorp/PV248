import http.client
from sys import argv
import json
import re
import time

def create_connection(port=8080, host=''):
    conn = http.client.HTTPConnection(host, port)
    conn.request("GET", "/list")
    response = conn.getresponse()
    string = response.read().decode('utf-8')
    json_data = json.loads(string)
    for game in json_data:
        if len(game['name']) > 0:
            print(str(game['id']) + ' ' + game['name'])
        else:
            print(str(game['id']))
    command = input('Type id number to join a game or type new to start a new game:')
    if command.startswith('new ') or command == 'new':
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
    running = check_game(game, player_number, conn)
    if running == 0:
        return
    elif running != player_number:
        while True:
            if cycle_check(game, player_number, conn) == 0:
                return
            take_turn(player_number, game, conn)
            if check_game(game, player_number, conn) == 0:
                return
    else:
        while True:
            take_turn(player_number, game, conn)
            if check_game(game, player_number, conn) == 0:
                return
            if cycle_check(game, player_number, conn) == 0:
                return

def cycle_check(game, player_number, conn):
    print("waiting for the other player")
    while True:
        time.sleep(1)
        conn.request("GET", "/status?game=" + str(game))
        response = conn.getresponse()
        if response.status == 404:
            print("invalid input")
            return 0
        string = response.read().decode('utf-8')
        json_data = json.loads(string)
        if 'winner' in json_data:
            if json_data['winner'] == player_number:
                print('you win')
            elif json_data['winner'] == 0:
                print('draw')
            else:
                print('you lose')
            return 0
        if json_data['next'] == player_number:
            print_board(json_data['board'])
            return json_data['next']


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
            print("invalid input")
            continue
        playing = False


def check_game(game, player_number, conn):
    conn.request("GET", "/status?game=" + str(game))
    response = conn.getresponse()
    if response.status == 404:
        print("invalid input")
        return 0
    string = response.read().decode('utf-8')
    json_data = json.loads(string)
    if 'winner' in json_data:
        if json_data['winner'] == player_number:
            print('you win')
        elif json_data['winner'] == 0:
            print('draw')
        else:
            print('you lose')
        return 0
    print_board(json_data['board'])
    return json_data['next']

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
