import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

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
    <div>
      <h1>Available Offers</h1>
      <div>
        <label>
          Search by Client ID (CIF/DNI):
          <input 
            type="text" 
            value={clientId} 
            onChange={handleClientIdChange} 
            disabled={offerId !== ''} // Disable if offerId is not empty
          />
        </label>
        <label>
          Search by Offer ID:
          <input 
            type="text" 
            value={offerId} 
            onChange={handleOfferIdChange} 
            disabled={clientId !== ''} // Disable if clientId is not empty
          />
        </label>
        <button onClick={filterOffers}>Search</button>
      </div>
      <ul>
        {filteredOffers.length > 0 ? (
          filteredOffers.map(offer => (
            <li key={offer.id_oferta}>
              <Link to={`/view-offer-details/${offer.id_oferta}`}>
                Offer ID: {offer.id_oferta}, Client ID: {offer.id_cliente}, Client Name: {offer.nombre_cliente}
              </Link>
            </li>
          ))
        ) : (
          <li>No offers found.</li>
        )}
      </ul>
    </div>
  );
};

export default ViewOffers;
