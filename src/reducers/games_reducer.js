export default function gamesReducer(
  state = { },
action) {
  switch(action.type) {
    case 'LOADING_GAME':
      return {
        ...state,
        loading: true
    }

    case 'GET_TIME':
      return {
        ...state,
        time: action.time
      }

    case 'GET_GAME':
      return {
        ...state,
        game: action.game
      }

    default:
      return state
  }
}
