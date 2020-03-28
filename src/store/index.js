import { createStore, applyMiddleware } from 'redux'
import rootReducer from '../reducers/index'
import thunk from 'redux-thunk';

let initialState = {
  game: { },
  player: {
    id: '',
    is_alive: true,
    in_game: false,
    name: '',
    color: ''
  }
}

const store = createStore(
  rootReducer,
  initialState,
  applyMiddleware(thunk)
)

export default  store
