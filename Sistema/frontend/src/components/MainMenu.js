// src/components/MainMenu.js
import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/MainMenu.css'; // Import the CSS file

const MainMenu = () => {
  return (
    <div className="main-menu-container">
      <div className="header">
        <h1>Menú Principal</h1>
      </div>
      <div className="main-menu-content">
        <Link to="/create-offer">
          <button>Crear nueva oferta</button>
        </Link>
        <Link to="/view-offers">
          <button>Consultar ofertas</button>
        </Link>
      </div>
    </div>
  );
};

export default MainMenu;
