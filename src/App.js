import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import store from './store/index'
import getTime from './actions/gameActions'

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
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p>The time at launch was {currentTime}.</p>
        <button onClick={dispatchBtnAction}>Test</button>
        <p>Current time is: {store.getState().game.time.time}</p>
      </header>
    </div>
  );
}

function dispatchBtnAction(e) {
  store.dispatch(getTime())
}

export default App;
