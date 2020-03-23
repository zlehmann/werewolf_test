import React, { Component } from 'react'
import { connect } from 'react-redux'
import store from '../store/index'
import { addPlayer } from '../actions/gameActions'
import { setPlayerName } from '../actions/playerActions'

const mapStateToProps = state => {
  return {
    game: state.game,
    player: state.player
  }
}

const mapDispatchToProps = dispatch => {
  return {
    addPlayer: (name) => {
      dispatch(addPlayer(name))
    },

    setPlayerName: (name, color) => {
      dispatch(setPlayerName(name, color))
    }
  }
}

class JoinGame extends Component {
  constructor(props) {
    super(props)
    this.state = ({
      name: 'New Player'
    })
  this.handleChange = this.handleChange.bind(this)
  this.handleSubmit = this.handleSubmit.bind(this)
  }

  handleChange(e) {
     this.setState({
       name: e.target.value
     })
  }

  handleSubmit(e) {
    e.preventDefault()
    // check if player name is taken already
    let checkName = true
    const players = store.getState().game.players
    players.forEach((player) => {
      if (this.state.name === player.name) {
        checkName = false
      }
    })

    // assign the next player color to new player
    const playerColor = store.getState().game.colors[store.getState().game.players.length]

    if (checkName === true) {
      // create new player object
      this.props.setPlayerName(this.state.name, playerColor)
      this.props.addPlayer(store.getState().player)
    } else {
      this.setState({
        name: 'New Player'
      })
      alert('This name is already taken, choose another name.')
    }

  }

  render() {

    return (
      <div id='join-game-form'>
        <form onSubmit={this.handleSubmit}>
          <h2>To join the game enter a name below</h2>
          <label>Enter Player Name:</label>
          <input type='text' name='playerName' onChange={this.handleChange} value={this.state.name}/><br/>
          <input type='submit' value='Submit'/>
        </form>
      </div>
    )
  }
}



export default connect(mapStateToProps, mapDispatchToProps)(JoinGame)
