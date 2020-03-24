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
    pass


class Player:
    def __init(self):
        self.is_alive = True


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
    if player not in game.players:
        game.players.append(player)
        # TODO: Create Session
        return "SUCCESS: {} has JOINED".format(player)
    else:
        return "FAILURE: {} has already JOINED".format(player), 400


@app.route('/game/start')
def start_game():
    if game.max_players >= len(game.players) >= game.min_players:
        game.state = GameState.VOTING
        return "GAME STARTED"


@app.route('/game/view')
def view_game():


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
