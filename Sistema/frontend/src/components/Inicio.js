import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Inicio.css';

const Inicio = () => {
    return (
    <div className="inicio-container">
      <img src="/resources/logo.png" alt="Company Logo" className="logo" />
      <h1>Sistema para la ayuda en la cotizacion de seguros de Responsabilidad Civil en Construcción</h1>
      <Link to="/login">
        <button className="login-button">Log In</button>
      </Link>
    </div>
    );
};

export default Inicio;
