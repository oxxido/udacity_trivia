import React, { Component } from 'react';
import logo from '../logo.svg';
import '../stylesheets/Header.css';

class Header extends Component {

  navTo(uri){
    window.location.href = window.location.origin + uri;
  }

  render() {
    return (
      <div className="App-header">
        <div onClick={() => {this.navTo('')}}>
          <img src="logo.png" className="logo" alt="Udacitrivia"/>
        </div>
        <h2 onClick={() => {this.navTo('')}}>List</h2>
        <h2 onClick={() => {this.navTo('/add')}}>Add</h2>
        <h2 onClick={() => {this.navTo('/play')}}>Play</h2>
      </div>
    );
  }
}

export default Header;
