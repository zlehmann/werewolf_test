export default function gamesReducer(
  state = {
    loading: false,
    name: '',
    players: [],
    state: '',
    colors: ['black', 'blue', 'brown', 'emerald', 'green', 'grey',
              'pink', 'purple', 'red', 'orange', 'teal'],
    round: 0,
    votes: []
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
