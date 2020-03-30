import time
from flask import Flask
from enum import Enum
from json import JSONEncoder
import json


class GameState(Enum):
    WAITING_FOR_PLAYERS = 1
    VOTING = 2
    RESOLVING = 3
    SHOWDOWN_VOTING = 4
    GAME_OVER = 5


class PlayerState(Enum):
    WAITING_FOR_GAME_START = 1
    VOTING = 2
    WAITING_FOR_OTHER_PLAYERS_TO_VOTE = 3
    DEAD = 4
    GAME_OVER = 5
    AMBUSH = 6


class Color(Enum):
    BLACK = 1
    BLUE = 2
    BROWN = 3
    EMERALD = 4
    GREEN = 5
    GREY = 6
    PINK = 7
    PURPLE = 8
    RED = 9
    ORANGE = 10
    TEAL = 11
    YELLOW = 12
    pass


class Player:
    def __init__(self, name):
        self.id = ''
        self.is_alive = True
        self.in_game = False
        self.name = name
        self.color = ''
    def reprJSON(self):
        return dict(id=self.id,
                    is_alive=self.is_alive,
                    in_game=self.in_game,
                    name=self.name,
                    color=self.color)

class Screen:
    pass


class Round:
    pass


class Game:
    def __init__(self):
        self.name = 'New Game'
        self.players = []
        self.state = GameState(1).name
        self.min_players = 6
        self.max_players = 12
        self.round = 0
        self.votes = []
    def reprJSON(self):
        return dict(name=self.name,
                    players=self.players,
                    state=self.state,
                    min_players=self.min_players,
                    max_players=self.max_players,
                    round=self.round,
                    votes=self.votes)

class ComplexEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)

app = Flask(__name__)
game = Game()


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@app.route('/game')
def get_game():
    return ComplexEncoder().encode(game)

@app.route('/game/join/<player>')
def join_game(player):
    new_player = Player(player)
    new_player.id = len(game.players) + 1
    new_player.in_game = True

    # validate new player joining
    valid_player = True
    error = ''
    for existing_player in game.players:
        if existing_player.name == new_player.name:
            valid_player = False
            error = 'Player name already exists'

    if new_player.id > game.max_players:
        valid_player = False
        error = 'Max number of players reached'

    if valid_player == True:
        new_player.color = Color(len(game.players) + 1).name
        game.players.append(new_player)
        # TODO: Create Session
        return ComplexEncoder().encode(new_player)
    else:
        return {'error': error}, 400

@app.route('/players/<id>')
def get_player(id):
    for player in game.players:
        if player.id == int(id):
            return ComplexEncoder().encode(player)

    return {'error': 'player not found'}

@app.route('/game/start')
def start_game():
    if game.max_players >= len(game.players) >= game.min_players:
        game.state = GameState.VOTING
        return ComplexEncoder().encode(game)


@app.route('/game/view')
def view_game():
    pass

@app.route('/vote/<voter>/<voted_for>')
def vote(voter, voted_for):
    pass


@app.route('/showdown/<voter>/<choice>')
def showdown(voter, showdown):
    pass

if __name__ == "__main__":
    app.run()

"""import connexion

app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('api.yaml')
app.run(port=5000)"""
