from api.app import *
import pytest



class TestApp:
    @pytest.fixture
    def game_with_min_players_not_started(self):
        test_game = Game()
        for i in range(game.min_players):
            test_game.join("test_player_{}".format(i))

        return test_game

    @pytest.fixture
    def game_with_min_players_started(self, game_with_min_players_not_started):
        test_game = game_with_min_players_not_started
        test_game.start()

        return test_game

    def test_game_can_only_start_with_minimum_number_of_players(self):
        test_game = Game()
        assert test_game.state is GameState.WAITING_FOR_PLAYERS
        for i in range(game.min_players):
            assert test_game.start().error == GameError.NOT_ENOUGH_PLAYERS
            test_game.join("test_player_{}".format(i))

        assert test_game.start().error is None

    def test_game_can_only_start_once(self):
        test_game = Game()
        for i in range(game.min_players):
            test_game.join("test_player_{}".format(i))

        test_game.start()
        assert test_game.start().error is GameError.GAME_ALREADY_STARTED

    def test_game_wont_let_more_than_max_players_join(self):
        test_game = Game()
        for i in range(game.max_players):
            test_game.join("test_player_{}".format(i))

        assert test_game.join("shouldn't_work").error is GameError.TOO_MANY_PLAYERS

    def test_game_starts_with_voting(self, game_with_min_players_not_started):
        test_game = game_with_min_players_not_started
        test_game.start()
        assert test_game.state is GameState.VOTING

    def test_first_voting_round_includes_all_players(self, game_with_min_players_started):
        test_game = game_with_min_players_started
        assert set(test_game.game_round.player_is_alive.keys()) == set(game_with_min_players_started.players.keys())


@pytest.fixture
def colors():
    return [
        Color.BLUE,
        Color.BLACK,
        Color.EMERALD,
        Color.PURPLE,
        Color.GREEN,
        Color.ORANGE,
        Color.YELLOW
    ]


class TestVotingRound:
    @pytest.fixture
    def voting_round(self, colors) -> VotingRound:
        return VotingRound(colors)

    def test_normal_vote(self, voting_round, colors):
        test_vote = voting_round.vote(colors[0], colors[1])
        assert test_vote.error is None

    def test_voter_cant_vote_twice(self, voting_round, colors):
        voting_round.vote(colors[0], colors[1])
        test_vote = voting_round.vote(colors[0], colors[2])
        assert test_vote.error is VoteError.VOTER_HAS_ALREADY_VOTED

    def test_voter_doesnt_exist(self, voting_round, colors):
        assert Color.PINK not in colors
        test_vote = voting_round.vote(Color.PINK, colors[0])
        assert test_vote.error is VoteError.VOTER_DOES_NOT_EXIST

    def test_voted_for_doesnt_exist(self, voting_round, colors):
        assert Color.PINK not in colors
        test_vote = voting_round.vote(colors[0], Color.PINK)
        assert test_vote.error is VoteError.VOTED_FOR_DOES_NOT_EXIST

    def test_voter_cant_vote_for_self(self, voting_round, colors):
        test_vote = voting_round.vote(colors[0], colors[0])
        assert test_vote.error is VoteError.CANNOT_VOTE_FOR_SELF

    def test_voter_can_ambush(self, voting_round, colors):
        test_vote = voting_round.vote(colors[0], Color.AMBUSH)
        assert test_vote.error is None

    def test_voting_round_not_over(self, voting_round, colors):
        for i in range(len(colors) - 1):
            voting_round.vote(colors[i], colors[i + 1])

        assert voting_round.everyone_has_voted() is False

    def test_voting_round_is_over(self, voting_round, colors):
        for i in range(len(colors)):
            voting_round.vote(colors[i], Color.AMBUSH)

        assert voting_round.everyone_has_voted() is True


class TestGameRound:
    @pytest.fixture
    def players(self, colors):
        return {colors[i]: Player(name=colors[i].name, player_id=i, color=colors[i]) for i in range(len(colors))}

    @pytest.fixture
    def game_round(self, players):
        game_round = GameRound(players)

        return game_round

    def test_game_round_can_start_voting_round_with_three_or_more_players_alive(self, game_round):
        assert game_round.start_voting_round().error is None

    def test_game_round_cant_start_voting_round_if_all_players_dead(self, game_round):
        for k in game_round.player_is_alive.keys():
            game_round.player_is_alive[k] = False

        assert game_round.check_num_alive() == 0
        assert game_round.start_voting_round().error is RoundError.INVALID_NUMBER_OF_PLAYERS_ALIVE

    def test_game_round_cant_start_voting_round_if_one_player_left_alive(self, game_round):
        one_alive = False
        for k in game_round.player_is_alive.keys():
            if one_alive is False:
                one_alive = True
                continue
            else:
                game_round.player_is_alive[k] = False

        assert game_round.check_num_alive() == 1
        assert game_round.start_voting_round().error is RoundError.INVALID_NUMBER_OF_PLAYERS_ALIVE

    def test_game_round_cant_start_voting_round_if_two_players_left_alive(self, game_round):
        two_alive = 0
        for k in game_round.player_is_alive.keys():
            if two_alive < 2:
                two_alive += 1
                continue
            else:
                game_round.player_is_alive[k] = False

        assert game_round.check_num_alive() == 2
        assert game_round.start_voting_round().error is RoundError.INVALID_NUMBER_OF_PLAYERS_ALIVE

class TestShowdown:
    @pytest.fixture
    def players(self, colors):
        return {colors[i]: Player(name=colors[i].name, player_id=i, color=colors[i]) for i in range(len(colors))}

    @pytest.fixture
    def showdown_round(self, players):
        showdown_round = ShowdownRound(players[0], players[1])
        return showdown_round

    def test_showdown_vote(self, showdown_round):
        assert showdown_round.showdown_vote(players[0], ShowdownChoice.SHARE).error is None
