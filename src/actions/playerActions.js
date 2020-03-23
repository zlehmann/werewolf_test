import store from '../store/index'

export function setPlayerName(name, color) {
  return (dispatch) => {
    dispatch({
      type: 'SET_PLAYER_NAME',
      name: name,
      color: color
    })
  }
}
