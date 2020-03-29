import React, { Component } from 'react'
import store from '../store/index'
import { connect } from 'react-redux'
import JoinGame from '../components/JoinGame'
import Game from './Game'
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

class Room extends Component {

  componentDidMount() {
    this.props.getGame()
  }

  render() {
    if(store.getState().player.in_game === false) {
      return (
        <div className='game'>
          <JoinGame />
        </div>
      )
    } else {
      return (
        <Game />
      )
    }

  }
}



export default connect(mapStateToProps, mapDispatchToProps)(Room)
