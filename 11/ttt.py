from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from urllib.parse import urlparse, parse_qs
from sys import argv
from http.cookies import SimpleCookie as cookie
import uuid
import json

class S(BaseHTTPRequestHandler):

    sessioncookies = {}
    boards = {}

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def _session_cookie(self, game_name,forcenew=False):
        for id, name in self.sessioncookies.items():
            if name == game_name:
                return id
        cookiestring = "\n".join(self.headers.get_all('Cookie',failobj=[]))
        c = cookie()
        c.load(cookiestring)
        c['session_id']=int(uuid.uuid1().int)
        self.sessioncookies[c['session_id'].value] = game_name
        self.boards[int(c['session_id'].value)] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        return c['session_id'].value

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _set_bad_response(self):
        self.send_error(404)

    def _who_is_next(self, board):
        player_one = 0
        player_two = 0
        for line in board:
            player_one += line.count(1)
            player_two += line.count(2)
        if player_one > player_two:
            return 2
        else:
            return 1

    def _evaluate_winner(self, board):

        draw = True

        for row in range(3):
            if 0 in board[row]:
                draw = False

        if draw:
            return 0

        for column in range(3):
            if board[0][column] > 0 and board[0][column] == board[1][column] == board [2][column]:
                return board[0][column]

        for row in range(3):
            if board[row][0] > 0 and board[row][0] == board[row][1] == board [row][2]:
                return board[row][0]

        if board[0][0] > 0 and board[0][0] == board[1][1] == board [2][2]:
            return board[0][0]

        if board[0][2] > 0 and board[0][2] == board[1][1] == board [2][0]:
            return board[0][2]

        return -1

    def _execute_start(self, query):
        parameters = parse_qs(query)
        id = -1
        if 'name' not in parameters:
            id = self._session_cookie("")
        else:
            game_name = parameters['name'][0]
            id = self._session_cookie(game_name)
        answer = {}
        answer['id'] = int(id)
        json_answer = json.dumps(answer)
        self._set_response()
        self.wfile.write("{}".format(json_answer).encode('utf-8'))

    def _execute_status(self, query):
        parameters = parse_qs(query)
        if 'game' not in parameters or parameters['game'][0] == '':
            self._set_bad_response()
        else:
            try:
                game_id = int(parse_qs(query)['game'][0])
            except ValueError:
                self._set_bad_response()
                return
            if game_id not in self.boards:
                self._set_bad_response()
            else:
                answer = {}
                answer_winner = {}
                board = self.boards[game_id]
                answer_winner['winner'] = self._evaluate_winner(board)
                if answer_winner['winner'] == -1:
                    answer['board'] = board
                    answer['next'] = self._who_is_next(board)
                    json_answer = json.dumps(answer)
                else:
                    json_answer = json.dumps(answer_winner)
                self._set_response()
                self.wfile.write("{}".format(json_answer).encode('utf-8'))

    def _execute_play(self, query):
        parameters = parse_qs(query)
        answer = {}
        if 'game' not in parameters or parameters['game'][0] == '':
            self._set_bad_response()
            return
        try:
            game = int(parameters['game'][0])
        except ValueError:
            self._set_bad_response()
            return
        if game not in self.boards:
            self._set_bad_response()
            return
        if 'player' not in parameters:
            answer['status'] = "bad"
            answer['message'] = "Parameter player is missing!"
        elif 'x' not in parameters:
            answer['status'] = "bad"
            answer['message'] = "Parameter x is missing!"
        elif 'y' not in parameters:
            answer['status'] = "bad"
            answer['message'] = "Parameter y is missing!"
        else:
            try:
                player = int(parameters['player'][0])
                x = int(parameters['x'][0])
                y = int(parameters['y'][0])
            except ValueError:
                answer['status'] = "bad"
                answer['message'] = "Some of the parameters are not integers!"
                json_answer = json.dumps(answer)
                self._set_response()
                self.wfile.write("{}".format(json_answer).encode('utf-8'))
                return
            if self._evaluate_winner(self.boards[game]) != -1:
                answer['status'] = "bad"
                answer['message'] = "This game has already finished!"
            elif player not in [1,2]:
                answer['status'] = "bad"
                answer['message'] = "This player does not exists!"
            elif x not in [0,1,2]:
                answer['status'] = "bad"
                answer['message'] = "Parameter x has to be 0 or 1 or 2!"
            elif y not in [0,1,2]:
                answer['status'] = "bad"
                answer['message'] = "Parameter y has to be 0 or 1 or 2!"
            elif self.boards[game][x][y] is not 0:
                answer['status'] = "bad"
                answer['message'] = "Given position is already taken!"
            elif self._who_is_next(self.boards[game]) != player:
                answer['status'] = "bad"
                answer['message'] = "It is not your turn!"
            else:
                self.boards[game][x][y] = player
                answer['status'] = "ok"
        json_answer = json.dumps(answer)
        self._set_response()
        self.wfile.write("{}".format(json_answer).encode('utf-8'))


    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/start":
            self._execute_start(parsed.query)
        elif parsed.path == "/status":
            self._execute_status(parsed.query)
        elif parsed.path == "/play":
            self._execute_play(parsed.query)
        else:
            self._set_bad_response()

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    #logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    #logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    try:
        port = int(argv[1])
        if port < 1:
            print("Second parameter has to be larger than zero")
        elif port > 65535:
            print("Second parameter has to be less than 65536")
        else:
            run(port=port)
    except ValueError:
        print("Second parameter has to be integer")
