import React, { Component } from 'react'
import store from '../store/index'
import { connect } from 'react-redux'
import JoinGame from '../components/JoinGame'

const mapStateToProps = state => {
  return {
    game: state.game,
    player: state.player
  }
}



class Room extends Component {
  render() {
    let page = null
    if(store.getState().player.inGame === false) {
      return (
        <div className='game'>
          <JoinGame />
        </div>
      )
    } else {
      return (
        <h1> game stage here </h1>
      )
    }

  }
}



export default connect(mapStateToProps)(Room)
