export default function playersReducer(
  state = {
    id: '',
    is_alive: true,
    in_game: false,
    name: '',
    color: ''
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
        player: action.payload
      }

    case 'GET_PLAYER':
      return {
        player: action.payload
      }

    default:
      return state
  }
}
