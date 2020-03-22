import store from '../store/index'

export default function getTime() {
  console.log('action getTime fired')
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

export function checkPlayerName(newName) {
  const players = store.getState().game.players
  players.push(newName)

  return (dispatch) => {
    dispatch({
      type: 'APPROVE_PLAYER_NAME',
      newName: players
    })
  }
}
