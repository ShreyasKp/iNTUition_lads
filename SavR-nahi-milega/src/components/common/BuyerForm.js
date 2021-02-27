import React from 'react';

function BuyerForm(props) {
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
  <input type="submit" className="btn btn-primary" value="Save" />
      </form>
);

}

export default BuyerForm
