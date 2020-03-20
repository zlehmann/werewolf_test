import { createStore, applyMiddleware } from 'redux'
import rootReducer from '../reducers/index'
import thunk from 'redux-thunk';

let initialState = {
  game: {
    loading: false,
    name: '',
    round: 0,
    phase: '',
    votes: [],
    goldCards: [],
    time: 999
  },
  player: {
    loading: false,
    name: '',
    color: 0,
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
