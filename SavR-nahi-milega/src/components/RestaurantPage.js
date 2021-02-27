import React, {useState} from 'react';
import Header from "./common/Header";
import RestaurantForm from "./common/RestaurantForm";
import { ToastContainer, toast } from 'react-toastify';
import Alert from 'react-bootstrap/Alert';

const RestaurantPage = props => {

  const [packet, setPacket] = useState({
    wt: "0.3g",
    numOfPacket: "",
    cuisine:"Asian"
  });

  function handleTitleChange(event) {
    const updatedPacket = {...packet, wt:event.target.value};
    setPacket(updatedPacket);
  }

  function handleNmChange(event) {
    const updatedPacket = {...packet, numOfPacket:event.target.value};
    setPacket(updatedPacket);
  }

  function handleCuisineChange(event) {
    const updatedPacket = {...packet, cuisine:event.target.value};
    setPacket(updatedPacket);
  }

  function handleChange(event) {
    const updatedPacket = {...packet, [event.target.name]:event.target.value};
    setPacket(updatedPacket);
  }

  function handleSubmit(event) {
    toast.success("Your form is submitted.");
    props.history.push("/");
    event.preventDefault();
  }


  return (
      <div>
      <h1>Restaurant Form</h1>
      <RestaurantForm packet={packet} onTitleChange={handleTitleChange} onNmChange={handleNmChange} onCuisineChange={handleCuisineChange} onSubmit={handleSubmit} />
    </div>
  );
}

export default RestaurantPage
