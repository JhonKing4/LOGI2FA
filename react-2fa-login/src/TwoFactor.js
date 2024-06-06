import React, { useState } from "react";
import axios from "axios";
import "./TwoFactor.css"; 

const TwoFactor = ({ setStep }) => {
  const [token, setToken] = useState("");
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setToken(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Token ingresado:", token);
    try {
      const response = await axios.post(
        "http://localhost:5000/api/two-factor",
        { token },
        { withCredentials: true }
      );
      setMessage(response.data.message);
      if (response.data.message === "2FA successful") {
        setStep(3);
      }
    } catch (error) {
      setMessage(
        error.response
          ? error.response.data.message
          : "Server error, please try again later."
      );
    }
  };

  return (
    <div className="two-factor-container">
      <h2>Autenticación de dos factores</h2>
      <form onSubmit={handleSubmit} className="two-factor-form">
        <div className="form-group">
          <label>Token:</label>
          <input
            type="text"
            value={token}
            onChange={handleChange}
            className="form-control"
          />
        </div>
        <button type="submit" className="btn-submit">
          Verificar
        </button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
};

export default TwoFactor;
