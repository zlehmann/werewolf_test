import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import store from './store/index'
import getTime from './actions/gameActions'
import Game from './containers/Game'

var avro = require('avro-js');

function App() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  return (
    <div className="App">
      <Game />

      <p>The time at launch was {currentTime}.</p>
      <button onClick={dispatchBtnAction}>Test</button>
      <p>Current time is: {store.getState().game.time.time}</p>
    </div>
  );
}

function dispatchBtnAction(e) {
  store.dispatch(getTime())
}

export default App;
