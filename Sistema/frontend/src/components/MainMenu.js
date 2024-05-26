// src/components/MainMenu.js
import React from 'react';
import { Link } from 'react-router-dom';

const MainMenu = () => {
  return (
    <div>
      <h1>Menú Principal</h1>
      <Link to="/create-offer">
        <button>Crear Nueva Oferta</button>
      </Link>
      <Link to="/view-offers">
        <button>Consultar Ofertas</button>
      </Link>
    </div>
  );
};

export default MainMenu;
