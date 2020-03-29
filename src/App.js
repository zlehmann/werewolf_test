import React, { useState, useEffect } from 'react';
import './App.css';
import Room from './containers/Room'

//var avro = require('avro-js');

function App() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  return (
    <div className="App">
      <Room />

      <p>The time at launch was {currentTime}.</p>
    </div>
  );
}

export default App;
