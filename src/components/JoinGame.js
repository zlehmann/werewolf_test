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
    console.log(this.state.name)
    fetch('/game/join/' + this.state.name)
      .then(res => res.json())
      .then(data => {console.log(data)})
    // need game action here to call get_game
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
