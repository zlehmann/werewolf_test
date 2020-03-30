export function getTime() {
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

export const getGame = () => {
  return (dispatch) => {
    return fetch('/game')
      .then(res => res.json())
      .then(resJSON =>
        {
          dispatch({
            type: 'GET_GAME',
            game: resJSON
          })
        })
  }
}

export function castVote(voter_id, voted_for_id) {
  return (dispatch) => {
    return fetch('/vote/' + voter_id + '/' + voted_for_id)
      .then(res => res.json())
      .then(resJSON => {
        dispatch({
          type: 'CAST_VOTE',
          payload: resJSON
        })
      })
  }
}
