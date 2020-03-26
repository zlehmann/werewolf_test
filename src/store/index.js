import { createStore, applyMiddleware } from 'redux'
import rootReducer from '../reducers/index'
import thunk from 'redux-thunk';

let initialState = {
  game: { },
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
