import React from 'react';
import HomePage from './HomePage';
import AboutPage from './AboutPage';
import RestaurantPage from './RestaurantPage';
import VolunteerPage from './VolunteerPage';
import BuyerPage from './BuyerPage';
import Header from './common/Header';
import { Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import "react-toastify/dist/ReactToastify.css";

function App() {

  return (
    <div className="container-fluid">
        <ToastContainer autoClose={3000} hideProgressBar />
        <Header />
        <Route path="/" exact component={HomePage} />
        <Route path="/about" component={AboutPage} />
        <Route path="/restaurant" component={RestaurantPage} />
        <Route path="/volunteer" component={VolunteerPage} />
        <Route path="/buyer" component={BuyerPage} />
    
    </div>
  );
}

export default App
