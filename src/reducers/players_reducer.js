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

    case 'CREATE_PLAYER':
      return {
        ...state,
        name: action.name,
        color: action.color,
        isAlive: true,
        inGame: true
      }

    default:
      return state
  }
}
