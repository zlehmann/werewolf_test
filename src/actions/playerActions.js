import store from '../store/index'

export function setPlayerName(name) {
  return (dispatch) => {
    dispatch({
      type: 'SET_PLAYER_NAME',
      name: name
    })
  }
}
