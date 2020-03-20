import { combineReducers } from 'redux'
import gamesReducer from './games_reducer'
import playersReducer from './players_reducer'


const rootReducer = combineReducers({
  game: gamesReducer,
  player: playersReducer
})

export default rootReducer
