import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import SidebarMenu from './SidebarMenu'; // Import the SidebarMenu component
import '../styles/ViewOffers.css'; // Import the CSS file

const ViewOffers = () => {
  const [offers, setOffers] = useState([]);
  const [filteredOffers, setFilteredOffers] = useState([]);
  const [clientId, setClientId] = useState('');
  const [offerId, setOfferId] = useState('');

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/ofertas_disponibles/')
      .then(response => {
        console.log('Offers data: ', response.data);
        setOffers(response.data);
        setFilteredOffers(response.data);
      })
      .catch(error => {
        console.error('Error fetching offers:', error);
      });
  }, []);

  const handleClientIdChange = (event) => {
    setClientId(event.target.value);
    if (event.target.value) {
      setOfferId(''); // Clear offerId if clientId is being set
    }
  };

  const handleOfferIdChange = (event) => {
    setOfferId(event.target.value);
    if (event.target.value) {
      setClientId(''); // Clear clientId if offerId is being set
    }
  };

  const filterOffers = () => {
    let filtered = offers;
    if (clientId) {
      filtered = filtered.filter(offer => offer.id_cliente === clientId);
    }
    if (offerId) {
      filtered = filtered.filter(offer => offer.id_oferta === parseInt(offerId));
    }
    setFilteredOffers(filtered);
  };

  return (
    <div className="view-offers-container">
      <SidebarMenu /> {/* Add the SidebarMenu component */}
      <div className="header">
        <h2>Ofertas disponibles</h2>
      </div>
      <div className="search-container">
        <h2>Buscar ofertas</h2>
        <label>
          Cliente (CIF/DNI):
          <input 
            type="text" 
            value={clientId} 
            onChange={handleClientIdChange} 
            disabled={offerId !== ''} // Disable if offerId is not empty
          />
        </label>
        <label>
          ID Oferta:
          <input 
            type="text" 
            value={offerId} 
            onChange={handleOfferIdChange} 
            disabled={clientId !== ''} // Disable if clientId is not empty
          />
        </label>
        <button onClick={filterOffers}>Buscar</button>
      </div>
      <div className="results-container">
        <h2>Resultados</h2>
        <table className="results-table">
          <thead>
            <tr>
              <th>ID Oferta</th>
              <th>ID Cliente</th>
              <th>Nombre cliente</th>
              <th>Detalles</th>
            </tr>
          </thead>
          <tbody>
            {filteredOffers.length > 0 ? (
              filteredOffers.map(offer => (
                <tr key={offer.id_oferta}>
                  <td>{offer.id_oferta}</td>
                  <td>{offer.id_cliente}</td>
                  <td>{offer.nombre_cliente}</td>
                  <td>
                    <Link to={`/view-offer-details/${offer.id_oferta}`}>Ver detalles</Link>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="4">No se han encontrado ofertas.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ViewOffers;
