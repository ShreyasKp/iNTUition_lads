import React from 'react';

function RestaurantForm(props) {
    return (
        <form onSubmit={props.onSubmit}>
          <div className="form-group">
            <label htmlFor="title">Weight per Packet</label>
            <div className="field">
              <input
                id="title"
                type="text"
                onChange={props.onTitleChange}
                name="title"
                className="form-control"
                value={props.packet.wt}
                />
            </div>
          </div>
                <div className="form-group">
      <label htmlFor="title">No of Packet</label>
  <div className="field">
      <input
  id="title"
  type="text"
  onChange={props.onNmChange}
  name="kol"
  className="form-control"
  value={props.packet.numOfPacket}
  />
  </div>
  </div>
  <div className="form-group">
    <label htmlFor="title">Cuisine</label>
  <div className="field">
      <select
  id="title"
  type="text"
  onChange={props.onCuisineChange}
  name="cuisine"
  className="form-control"
  value={props.packet.cuisine}>
    <option value="Asian">Asian</option>
            <option value="Chinese">Chinese</option>
            <option value="Italian">Italian</option>
            <option value="Thai">Thai</option>
            <option value="North Indian">North Indian</option>
    </select>
  </div>
  </div>
  
      <input type="submit" className="btn btn-primary" value="Save" />
        </form>
  );

}

export default RestaurantForm
