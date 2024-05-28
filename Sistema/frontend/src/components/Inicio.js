import React from 'react';
import { Link } from 'react-router-dom';

const Inicio = () => {
    return (
    <div>
      <h1>Sistema para la ayuda en la cotizacion de seguros de Responsabilidad Civil en Construcción</h1>
      <Link to="/login">
        <button>Log In</button>
      </Link>
    </div>
    );
};

export default Inicio