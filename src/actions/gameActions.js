import store from '../store/index'

export default function getTime() {
  return (dispatch) => {
    return fetch('/time')
    .then(res => res.json())
    .then(resJSON =>
      {
        dispatch({
          type: 'GET_TIME',
          time: resJSON
        })
      })
    }
  }

export function addPlayer(newName) {
  const players = store.getState().game.players
  players.push(newName)

  return (dispatch) => {
    dispatch({
      type: 'ADD_PLAYER',
      newName: players
    })
  }
}
