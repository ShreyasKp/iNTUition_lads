import React, { Component } from 'react';
import logo from '../Gmaps.png';
export default class Header extends Component {
  render() {
    return (
      <div className="row">
        <div className="logo">
          <img src={logo} width="1000" height="1000" />
        </div>
      </div>
    );
  }
} 
