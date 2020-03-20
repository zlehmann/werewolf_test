export default function gamesReducer(
  state = {
    loading: false,
    name: '',
    round: 0,
    phase: '',
    votes: [],
    goldCards: [],
    time: 0
  },
action) {
  switch(action.type) {
    case 'LOADING_GAME':
      return {
        ...state,
        loading: true
    }

    case 'GET_TIME':
      console.log('reducer handling get time request', action.time)
      return {
        ...state,
        time: action.time
      }

    default:
      return state
  }
}
