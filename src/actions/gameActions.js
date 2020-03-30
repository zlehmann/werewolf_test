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
  console.log('get game')
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
