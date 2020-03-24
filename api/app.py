import time
from flask import Flask
from enum import Enum


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
    def __init__(self):
        self.is_alive = True
        self.name = ''
        self.color = ''


class Screen:
    pass


class Round:
    pass


class Game:
    def __init__(self):
        self.players = []
        self.state = GameState.WAITING_FOR_PLAYERS
        self.min_players = 6
        self.max_players = 12
        self.round = 0
        self.votes = []


app = Flask(__name__)
game = Game()


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@app.route('/game')
def get_game():
    return {'players': game.players}


@app.route('/game/join/<player>')
def join_game(player):
    new_player = Player()
    new_player.name = player
    new_player.color = Color(len(game.players) + 1).name
    if new_player not in game.players:
        game.players.append(new_player)
        # TODO: Create Session
        return {'player': {'name': new_player.name, 'color': new_player.color}}
    else:
        return {'player_creation': 'FAILURE'}, 400


@app.route('/game/start')
def start_game():
    if game.max_players >= len(game.players) >= game.min_players:
        game.state = GameState.VOTING
        return "GAME STARTED"


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
