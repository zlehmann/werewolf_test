export default function getTime() {
  console.log('action fired')
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
