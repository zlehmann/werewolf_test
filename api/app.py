import time
from flask import Flask
from enum import Enum
from json import JSONEncoder
import json
import itertools


class GameState(Enum):
    WAITING_FOR_PLAYERS = 0
    VOTING = 1
    RESOLVING = 2
    SHOWDOWN_VOTING = 3
    GAME_OVER = 4


class PlayerState(Enum):
    WAITING_FOR_GAME_START = 0
    VOTING = 1
    WAITING_FOR_OTHER_PLAYERS_TO_VOTE = 2
    DEAD = 3
    GAME_OVER = 4
    AMBUSH = 5


class Color(Enum):
    BLACK = 0
    BLUE = 1
    BROWN = 2
    EMERALD = 3
    GREEN = 4
    GREY = 5
    PINK = 6
    PURPLE = 7
    RED = 8
    ORANGE = 9
    TEAL = 10
    YELLOW = 11
    AMBUSH = 99  # This just makes it easy to have a special case for ambush



class Player:
    def __init__(self, name, player_id, color):
        self.id = player_id
        self.is_alive = True
        self.name = name
        self.color: Color = color

    def to_json(self):
        return dict(id=self.id,
                    is_alive=self.is_alive,
                    name=self.name,
                    color=self.color.name)

class Screen:
    pass


class Round:
    pass


class Game:
    def __init__(self):
        self.players: dict[Color, Player] = {}
        self.state = GameState.WAITING_FOR_PLAYERS
        self.min_players = 6
        self.max_players = 12
        self.round = 0
        self.votes = {}

    def start_voting_round(self):
        if self.state is not GameState.VOTING:
            raise Exception("Not valid voting round")
        else:
            self.votes = {player: [] for player in self.players}
            self.votes[Color.AMBUSH] = []

    def vote(self, voter_id, voted_for_id):
        voter_id = Color(voter_id)
        voted_for_id = Color(voted_for_id)
        if self.state is not GameState.VOTING:
            return {"error": "Game state should be VOTING, actually: {}".format(self.state.name)}
        elif not self.players[voter_id].is_alive:
            return {"error": "Player is dead"}
        elif voter_id is voted_for_id:
            return {"error", "Player can't vote for themselves"}
        elif Color(voted_for_id) is not Color.AMBUSH and voted_for_id.value >= len(self.players):
            return {"error", "Invalid player id: {}".format(voted_for_id)}
        elif not self.players[voted_for_id].is_alive:
            return {"error": "Voted for player: {} is already dead".format(voted_for_id)}
        elif voter_id in (item for sublist in self.votes.values() for item in sublist):
            return {"error": "{} has already voted".format(voter_id)}
        else:
            self.votes[voted_for_id].append(voter_id)
            return {"message": "{} voted for {}".format(voter_id, voted_for_id)}

    def everyone_has_voted(self):
        #if list(self.players.keys()).sort == list([item for sublist in self.votes.values() for item in sublist]):
        if len(self.players.keys()) == len(list([item for sublist in self.votes.values() for item in sublist])):
            return True
        else:
            return False

    def resolve_vote(self):
        # FIXME: Below should be simplified, but my brain is mush
        votes_by_number = {k: len(v) for k, v in self.votes.items() if k is not Color.AMBUSH}
        plurality = max(votes_by_number.values())
        players_voted_for_with_plurality = [player for player in votes_by_number.keys() if votes_by_number[player] == plurality]
        temp = []
        for player in players_voted_for_with_plurality:
            temp.append([voter for voter in self.votes[player]])

        players_who_voted_for_plurality = list(itertools.chain(*temp))
        players_who_didnt_vote_for_plurality = list(set(self.players.keys()).difference(set(players_who_voted_for_plurality)))
        players_who_ambushed_with_plurality = [player for player in players_voted_for_with_plurality if player in self.votes[Color.AMBUSH]]
        voted_for_to_die = [player for player in players_voted_for_with_plurality if player not in players_who_ambushed_with_plurality]
        players_to_die = set(voted_for_to_die + players_who_didnt_vote_for_plurality)
        # TODO: Ambush logic should go somewhere here but for now just kill all players who didn't ambush
        for player in players_to_die:
            game.players[player].is_alive = False

        return players_to_die


    def to_json(self):
        return dict(players=convert_keys(self.players),
                    state=self.state,
                    min_players=self.min_players,
                    max_players=self.max_players,
                    round=self.round,
                    votes=convert_keys(self.votes))


def convert_keys(obj, convert=str):
    if isinstance(obj, list):
        return [convert_keys(i, convert) for i in obj]
    if not isinstance(obj, dict):
        return obj
    return {k.name: convert_keys(v, convert) for k, v in obj.items()}


class ComplexEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        elif isinstance(obj, Enum):
            return obj.name
        else:
            return json.JSONEncoder.default(self, obj)


app = Flask(__name__)
game = Game()


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@app.route('/game')
def get_game():
    return ComplexEncoder().encode(convert_keys(game))


@app.route('/game/join/<player>')
def join_game(player):
    if len(game.players.keys()) == game.max_players:
        return {'error': "Max number of players reached"}, 400
    elif game.state is not GameState.WAITING_FOR_PLAYERS:
        return {'error': "Game already started"}, 400
    elif player in (x.name for x in game.players.values()):
        return {'error': 'Player name already exists'}, 400
    else:
        player_id = len(game.players.keys())
        new_player = Player(player, player_id, Color(player_id))
        game.players[new_player.color] = new_player
        # TODO: Create Session
        return ComplexEncoder().encode(convert_keys(new_player))


@app.route('/players/<int:player_id>')
def get_player(player_id):
    print(player_id, Color(player_id))
    player = next((v for k, v in game.players.items() if k == Color(player_id)), None)
    return ComplexEncoder().encode(convert_keys(player)) if player else ({'error': 'player not found'}, 400)


@app.route('/game/start')
def start_game():
    if game.state is not GameState.WAITING_FOR_PLAYERS:
        return {"error": "Game has already started"}, 400
    elif len(game.players) < game.min_players:
        return {"error": "Only {} players have joined. Need at least {} players".format(len(game.players),
                                                                                        game.min_players)}, 400
    else:
        game.state = GameState.VOTING
        game.start_voting_round()
        return {"message": "GAME STARTED"}


@app.route('/game/view')
def view_game():
    pass


@app.route('/vote/<int:voter_id>/<int:voted_for_id>')
def vote(voter_id, voted_for_id):
    this_vote = game.vote(voter_id, voted_for_id)
    if "error" in this_vote:
        return this_vote, 400
    else:
        if game.everyone_has_voted():
            game.resolve_vote()

        return this_vote

    # return (this_vote, 400) if "error" in this_vote else this_vote


@app.route('/showdown/<int:voter>/<int:choice>')
def showdown(voter, showdown):
    pass



@app.route('/game/new')
def new_game():
    global game
    game = Game()
    return "new game started"


@app.route('/test/new_game')
def test_new_game():
    new_game()
    for player in ["A", "B", "C", "D", "E", "F"]:
        join_game(player)

    return ComplexEncoder().encode(game)

@app.route('/test/voting')
def test_voting():
    test_new_game()
    start_game()
    print(vote(0, 1))
    print(vote(1, 2))
    print(vote(2, 1))
    print(vote(3, 1))
    print(vote(4, 1))
    print(vote(5, 1))
    return ComplexEncoder().encode(game)


if __name__ == "__main__":
    app.run()

"""import connexion

app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('api.yaml')
app.run(port=5000)"""
