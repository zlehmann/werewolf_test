export default function playersReducer(
  state = {
    loading: false,
    inGame: false,
    name: '',
    color: 0,
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
        name: action.name
      }

    default:
      return state
  }
}
