export function createPlayer(name, color) {
  return (dispatch) => {
    dispatch({
      type: 'CREATE_PLAYER',
      name: name,
      color: color
    })
  }
}
