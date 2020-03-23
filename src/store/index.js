import { createStore, applyMiddleware } from 'redux'
import rootReducer from '../reducers/index'
import thunk from 'redux-thunk';

let initialState = {
  game: {
    loading: false,
    name: '',
    players: [],
    colors: ['black', 'blue', 'brown', 'emerald', 'green', 'grey',
              'pink', 'purple', 'red', 'orange', 'teal'],
    round: 0,
    phase: '',
    votes: [],
    goldCards: [],
    time: 999
  },
  player: {
    loading: false,
    inGame: false,
    name: '',
    color: '',
    vote: '',
    points: 0
  }
}

const store = createStore(
  rootReducer,
  initialState,
  applyMiddleware(thunk)
)

export default  store
