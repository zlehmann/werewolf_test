export default function gamesReducer(
  state = {
    loading: false,
    name: '',
    players: [],
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
      return {
        ...state,
        time: action.time
      }

    case 'APPROVE_PLAYER_NAME':
      return Object.assign({}, state, {
        players: action.newName
      })

    case 'DISAPPROVE_PLAYER_NAME':
      return {
        ...state,

      }

    default:
      return state
  }
}
