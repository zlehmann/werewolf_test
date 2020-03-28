export function createPlayer(player) {
  return (dispatch) => {
    dispatch({
      type: 'CREATE_PLAYER',
      payload: player
    })
  }
}

export function getPlayer(id) {
  return (dispatch) => {
    return fetch('/players/' + id)
      .then(res => res.json())
      .then(resJSON =>
        {
          dispatch({
            type: 'GET_PLAYER',
            payload: resJSON
          })
        })
  }
}
