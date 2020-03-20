export default function playersReducer(
  state = {
    loading: false,
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

    default:
      return state
  }
}
