export default function playersReducer(
  state = {
    loading: false,
    is_alive: true,
    in_game: true,
    name: '',
    color: '',
    vote: '',
    points: 0
  },
action) {
  switch(action.type) {
    case 'LOADING_GAME':
      return {
        ...state,
        loading: true
    }

    case 'SET_PLAYER_NAME':
      return {
        ...state,
        name: action.name,
        color: action.color,
        inGame: true
      }

    default:
      return state
  }
}
