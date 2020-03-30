import React, { Component } from 'react'
import store from '../store/index'
import { connect } from 'react-redux'
import { getGame } from '../actions/gameActions'
import { getPlayer } from '../actions/playerActions'
import { withPolling } from '../withPolling'
import VotingBooth from '../components/VotingBooth'

const mapStateToProps = state => {
  return {
    game: state.game,
    player: state.player
  }
}

const mapDispatchToProps = dispatch => {
  return {
    getGame: () => {
      dispatch(getGame())
    },
    getPlayer: (id) => {
      dispatch(getPlayer(id))
    }
  }
}

class Game extends Component {

  componentDidMount() {
    this.props.getGame()
    this.props.getPlayer(this.props.player.player.id)
  }

  render() {
    const players = Object.values(this.props.game.game.players)
    const listPlayers = players.map((player) =>
      <li key={player.id}>{player.name}, {player.color}</li>
    )
    const player = this.props.player.player

    const voting = ((store.getState().game.game.state === 'VOTING') ? <VotingBooth /> : null)

    return(
      <div>
        <div>
          <h1>{this.props.game.game.name}</h1>
          <h2>Players:</h2>
          <ol>{listPlayers}</ol>
        </div>

        <div>
          <h2>You are player #{player.id + 1}</h2>
          <p>other stats can go here</p>
        </div>

        {voting}
      </div>
    )
  }
}



export default withPolling(getGame)(connect(mapStateToProps, mapDispatchToProps)(Game))
