import React, { Component } from 'react'
import { connect } from 'react-redux'

const mapStateToProps = state => {
  return {
    game: state.game,
    player: state.player
  }
}

class VotingBooth extends Component {

  render() {
    const players = Object.values(this.props.game.game.players)
    const livingPlayers = players.map((player) => {
      if (player.is_alive === true) {
        return (
          <div>
            <p>{player.color}</p>
          </div>
        )
      }
    })

    return (
      <div>
        <h3>Vote for a player:</h3>
        {livingPlayers}
      </div>
    )
  }
}

export default connect(mapStateToProps)(VotingBooth)
