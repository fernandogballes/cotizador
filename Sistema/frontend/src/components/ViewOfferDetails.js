import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import '../styles/ViewOfferDetails.css'; // Import the CSS file

const ViewOfferDetails = () => {
    const { id } = useParams();
    const [offer, setOffer] = useState(null);

    useEffect(() => {
        const fetchOfferDetails = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/api/oferta_detalle_completo/${id}/`);
                setOffer(response.data);
            } catch (error) {
                console.error('Error fetching the offer details:', error);
            }
        };

        fetchOfferDetails();
    }, [id]);

    if (!offer) {
        return <div>Loading...</div>;
    }

    return (
        <div className="view-offer-details-container">
            <div className="header">
                <h2>Detalles de la oferta</h2>
            </div>
            <div className="details-container">
                <h3>Datos del Cliente</h3>
                <p><strong>Nombre:</strong> {offer.nombre_cliente}</p>
                <p><strong>Semáforo:</strong> {offer.semaforo}</p>
                <p><strong>Suma asegurada:</strong> {offer.suma_asegurada}</p>
                <p><strong>Límite por anualidad:</strong> {offer.limite_anualidad}</p>
            </div>
            <div className="coverages-container">
                <h3>Coberturas</h3>
                <ul>
                    {offer.coberturas.map((coverage, index) => (
                        <li key={index}>
                            <p><strong>Cobertura:</strong> {coverage.nombre_cobertura}</p>
                            <p><strong>Franquicia:</strong> {coverage.franquicia}</p>
                            <p><strong>Sublimite:</strong> {coverage.sublimite}</p>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default ViewOfferDetails;
