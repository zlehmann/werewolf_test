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
    this.state = ({
      vote: '',
      error: ''
    })
    this.handleVote = this.handleVote.bind(this)
  }

  handleVote(voter_id, voted_for_id) {
    this.props.castVote(voter_id, voted_for_id)
    fetch('/players/' + voted_for_id)
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          this.setState({
            vote: 'Invalid',
            error: data.error
          })
        } else {
          this.setState({
            vote: data.name
          })
        }
      })
  }

  render() {
    const players = Object.values(this.props.game.game.players)
    const eligiblePlayers = players.map((player) => {
      if (player.is_alive === true) {
        return (
          <div key={player.id} className='vote-block' onClick={
            () => {this.handleVote(this.props.player.player.id, player.id)}}>
            <p>{player.color}</p>
          </div>
        )
      }
    })

    if (this.state.vote === '') {
      return (
        <div>
          <h3>Vote for a player:</h3>
          {eligiblePlayers}
        </div>
      )
    } else {
      return (
        <div>
          <h3>You voted for:</h3>
          {this.state.vote}
        </div>
      )
    }
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(VotingBooth)
