import React, { Component } from 'react'
import { connect } from 'react-redux'
import { getPlayer } from '../actions/playerActions'
import { castVote } from '../actions/gameActions'

const mapStateToProps = state => {
  return {
    game: state.game,
    player: state.player
  }
}

const mapDispatchToProps = dispatch => {
  return {
    getPlayer: (id) => {
      dispatch(getPlayer(id))
    },

    castVote: (voter_id, voted_for_id) => {
      dispatch(castVote(voter_id, voted_for_id))
    }
  }
}

class VotingBooth extends Component {
  constructor(props) {
    super(props)
    this.handleVote = this.handleVote.bind(this)
  }

  handleVote(voter_id, voted_for_id) {
    this.props.castVote(voter_id, voted_for_id)
  }

  render() {
    const players = Object.values(this.props.game.game.players)
    const livingPlayers = players.map((player) => {
      if (player.is_alive === true) {
        return (
          <div key={player.id} className='vote-block' onClick={
            () => {this.handleVote(this.props.player.player.id, player.id)}}>
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

export default connect(mapStateToProps, mapDispatchToProps)(VotingBooth)
