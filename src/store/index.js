import { createStore, applyMiddleware } from 'redux'
import rootReducer from '../reducers/index'
import thunk from 'redux-thunk';

let initialState = {
  game: {
    loading: false,
    name: '',
    players: [],
    state: '',
    round: 0,
    votes: []
  },
  player: {
    loading: false,
    isAlive: true,
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
