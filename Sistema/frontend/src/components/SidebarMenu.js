import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/SidebarMenu.css'; // Import the CSS file

const SidebarMenu = () => {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const handleLogout = () => {
    // Clear session or authentication tokens here
    localStorage.removeItem('authToken'); // Example: removing token from localStorage
    navigate('/'); // Redirect to the home page
  };

  return (
    <div>
      <div className="hamburger-icon" onClick={toggleMenu}>
        &#9776; {/* Unicode for hamburger icon */}
      </div>
      <div className={`sidebar-menu ${isOpen ? 'open' : ''}`}>
        <Link to="/menu" onClick={toggleMenu}>Inicio</Link>
        <Link to="/create-offer" onClick={toggleMenu}>Crear nueva oferta</Link>
        <Link to="/view-offers" onClick={toggleMenu}>Consultar ofertas</Link>
        <button className="logout-button" onClick={handleLogout}>Log out</button>
      </div>
    </div>
  );
};

export default SidebarMenu;
