import React, { Component } from 'react'
import store from '../store/index'
import { connect } from 'react-redux'
import { getGame } from '../actions/gameActions'

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
    }
  }
}

class Game extends Component {

  componentDidMount() {
    this.props.getGame()
  }

  render() {
    const players = this.props.game.game.players
    const listPlayers = players.map((player) =>
      <li>{player.name}, {player.color}</li>
    )

    return(
      <div>
        <h1>{this.props.game.game.name}</h1>
        <h2>Players:</h2>
        <ol>{listPlayers}</ol>
      </div>
    )
  }
}



export default connect(mapStateToProps, mapDispatchToProps)(Game)
