import time
from flask import Flask
from enum import Enum
from json import JSONEncoder
from typing import List, Dict, Optional
import json
import itertools
import functools


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

class ShowdownChoice(Enum):
    SHARE = 0
    STEAL = 1
    TAKE_ONE_AND_GO = 2


class GameError(Enum):
    NOT_ENOUGH_PLAYERS = 0
    TOO_MANY_PLAYERS = 1
    GAME_ALREADY_STARTED = 2
    PLAYER_NAME_ALREADY_USED = 3
    INCORRECT_GAME_STATE = 4
    PLAYER_DEAD = 5
    INVALID_PLAYER_CHOICE = 6
    PLAYER_ALREADY_VOTED = 7


class VoteError(Enum):
    VOTER_DOES_NOT_EXIST = 0
    CANNOT_VOTE_FOR_SELF = 1
    VOTED_FOR_DOES_NOT_EXIST = 2
    VOTER_HAS_ALREADY_VOTED = 3
    VOTER_IS_DEAD = 4
    VOTED_FOR_IS_DEAD =5


class RoundStatus(Enum):
    EVERYONE_DEAD = 0
    ONE_PLAYER_ALIVE = 1
    TWO_PLAYERS_ALIVE = 2
    MORE_THAN_TWO_PLAYERS_ALIVE = 3


class RoundError(Enum):
    INVALID_NUMBER_OF_PLAYERS_ALIVE = 0


# FIXME: Convert much of below to python dataclass
class GameMessage:
    def __init__(self, error: GameError = None, message: str = None, data: dict = None):
        self.error: GameError = error
        self.message: str = message
        self.data: dict = data

    def to_json(self):
        return dict(error=self.error, message=self.message, data=self.data)


class VoteMessage:
    def __init__(self, error: VoteError = None):
        self.error: VoteError = error

    def to_json(self):
        return dict(error=self.error)


class RoundMessage:
    def __init__(self, error=None, voting_over: bool = False):
        self.error = error
        self.over = voting_over


class Player:
    def __init__(self, name, player_id, color):
        self.id = player_id
        self.name = name
        self.color: Color = color

    def to_json(self):
        return dict(id=self.id,
                    name=self.name,
                    color=self.color.name)


class Screen:
    pass


class ShowdownRound:
    def __init__(self, player_one: Color, player_two: Color, choices: List[ShowdownChoice]):
        self.player_one = player_one
        self.player_two = player_two
        self.showdown_votes = {choice: [] for choice in choices}

    def showdown_vote(self, voter: Color, voted_for: Color):
        if self.votes.get(voter) is None:
            return VoteMessage(error=VoteError.VOTER_DOES_NOT_EXIST)
        elif self.votes.get(voted_for) is None:
            return VoteMessage(error=VoteError.VOTED_FOR_DOES_NOT_EXIST)
        elif voter == voted_for:
            return VoteMessage(error=VoteError.CANNOT_VOTE_FOR_SELF)
        elif self.has_voted[voter]:
            return VoteMessage(error=VoteError.VOTER_HAS_ALREADY_VOTED)
        else:
            self.votes.get(voted_for).append(voter)
            self.has_voted[voter] = True
            return VoteMessage()


# A game round consists of multiple voting rounds. It ends in either a new game round with everyone back to life,
# a showdown round or a player winning the game
class GameRound:
    def __init__(self, players: Dict[Color, Player]):
        self.player_is_alive = {color: True for color, _ in players.items()}
        self.voting_round: Optional[VotingRound] = None
        self.showdown_round: Optional[ShowdownRound] = None

    def start_voting_round(self):
        if self.check_round_status() is not RoundStatus.MORE_THAN_TWO_PLAYERS_ALIVE:
            return RoundMessage(error=RoundError.INVALID_NUMBER_OF_PLAYERS_ALIVE, voting_over=True)
        else:
            self.voting_round = VotingRound([
                color for color in self.player_is_alive.keys() if self.player_is_alive[color] is True]
            )
            return RoundMessage(voting_over=False)

    # TODO: Implement Me
    def start_showdown(self):
        if self.check_round_status() is not RoundStatus.TWO_PLAYERS_ALIVE:
            return RoundMessage(error=RoundError.INVALID_NUMBER_OF_PLAYERS_ALIVE)
        else:
            self.showdown_round = ShowdownRound(
                color for color in self.player_is_alive.keys() if self.player_is_alive[color] is True]
            )  # FIXME: Finish implementation
            return RoundMessage()

    def vote(self, voter: Color, voted_for: Color):
        vote_message = self.voting_round.vote(voter, voted_for)
        if vote_message.error:
            # TODO: Should I return a "gameround" message?
            return RoundMessage(error=vote_message.error)

        if self.voting_round.everyone_has_voted():
            for killed in self.voting_round.resolve_vote():
                self.player_is_alive[killed] = False
                return RoundMessage(voting_over=True)
        else:
            return RoundMessage(voting_over=False)

    def check_round_status(self):
        num_alive = self.check_num_alive()
        if num_alive == 0:
            return RoundStatus.EVERYONE_DEAD
        elif num_alive == 1:
            return RoundStatus.ONE_PLAYER_ALIVE
        elif num_alive == 2:
            return RoundStatus.TWO_PLAYERS_ALIVE
        elif num_alive > 2:
            return RoundStatus.MORE_THAN_TWO_PLAYERS_ALIVE

    def check_num_alive(self):
        return sum(1 for i in self.player_is_alive.values() if i)


class VotingRound:
    def __init__(self, colors: List[Color]):
        self.colors = colors
        self.has_voted: Dict[Color, bool] = {color: False for color in colors}
        self.votes = {color: [] for color in colors}
        self.votes[Color.AMBUSH] = []

    def vote(self, voter: Color, voted_for: Color):
        if self.votes.get(voter) is None:
            return VoteMessage(error=VoteError.VOTER_DOES_NOT_EXIST)
        elif self.votes.get(voted_for) is None:
            return VoteMessage(error=VoteError.VOTED_FOR_DOES_NOT_EXIST)
        elif voter == voted_for:
            return VoteMessage(error=VoteError.CANNOT_VOTE_FOR_SELF)
        elif self.has_voted[voter]:
            return VoteMessage(error=VoteError.VOTER_HAS_ALREADY_VOTED)
        else:
            self.votes.get(voted_for).append(voter)
            self.has_voted[voter] = True
            return VoteMessage()

    def everyone_has_voted(self):
        return functools.reduce(lambda a, b: a and b, self.has_voted.values())

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

        return players_to_die


class Game:
    def __init__(self):
        self.players: dict[Color, Player] = {}
        self.state = GameState.WAITING_FOR_PLAYERS
        self.min_players = 6
        self.max_players = 12
        self.game_round: Optional[GameRound] = None
        self.round = 0

    def join(self, name):
        if len(self.players.keys()) == self.max_players:
            return GameMessage(error=GameError.TOO_MANY_PLAYERS, message="Max number of players reached")
        elif self.state is not GameState.WAITING_FOR_PLAYERS:
            return GameMessage(error=GameError.GAME_ALREADY_STARTED, message="Game already started")
        elif name in (x.name for x in self.players.values()):
            return GameMessage(error=GameError.PLAYER_NAME_ALREADY_USED, message='Player name already exists')
        else:
            player_id = len(self.players.keys())
            new_player = Player(name, player_id, Color(player_id))
            self.players[new_player.color] = new_player
            # TODO: Create Session
            return GameMessage(data=ComplexEncoder().encode(convert_keys(new_player)), message="{} has joined".format(name))

    def start(self) -> GameMessage:
        if self.state is not GameState.WAITING_FOR_PLAYERS:
            return GameMessage(error=GameError.GAME_ALREADY_STARTED, message="Game already started")
        elif len(self.players.keys()) < self.min_players:
            return GameMessage(error=GameError.NOT_ENOUGH_PLAYERS,
                               message="Only {} players have joined. Need at least {} players".format(len(self.players),
                                                                                            self.min_players))
        else:
            self.state = GameState.VOTING
            self.start_game_round()
            return GameMessage(data=self.to_json(), message="Game started")

    def start_game_round(self):
        if self.state is not GameState.VOTING:
            return GameMessage(error=GameError.INCORRECT_GAME_STATE)
        else:
            self.game_round = GameRound(self.players)
            return GameMessage(message="New Round started")

    def vote(self, voter, voted_for):
        voter = Color(voter)
        voted_for = Color(voted_for)
        return self.game_round.vote(voter, voted_for)

    def to_json(self):
        return dict(players=convert_keys(self.players),
                    state=self.state,
                    min_players=self.min_players,
                    max_players=self.max_players,
                    round=self.round)


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

"""@app.route('/test/voting')
def test_voting():
    test_new_game()
    start_game()
    print(vote(0, 1))
    print(vote(1, 2))
    print(vote(2, 1))
    print(vote(3, 1))
    print(vote(4, 1))
    print(vote(5, 1))
    return ComplexEncoder().encode(game)"""


if __name__ == "__main__":
    app.run()

"""import connexion

app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('api.yaml')
app.run(port=5000)"""
