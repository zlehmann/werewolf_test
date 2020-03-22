import React, { Component } from 'react'
import { connect } from 'react-redux'
import store from '../store/index'
import { checkPlayerName } from '../actions/gameActions'

const mapStateToProps = state => {
  return {
    game: state.game,
    player: state.player
  }
}

const mapDispatchToProps = dispatch => {
  return {
    checkPlayerName: (name) => {
      dispatch(checkPlayerName(name))
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
    let checkName = true
    const players = store.getState().game.players
    players.forEach((player) => {
      if (this.state.name === player) {
        checkName = false
      }
    })

    if (checkName === true) {
      this.props.checkPlayerName(this.state.name)
      //set player name here
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
