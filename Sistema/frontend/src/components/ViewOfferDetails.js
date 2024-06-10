import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import SidebarMenu from './SidebarMenu'; // Import the SidebarMenu component
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

    const getSemaforoColor = (semaforo) => {
        switch (semaforo) {
            case 1:
                return 'red';
            case 2:
                return 'yellow';
            case 3:
                return 'green';
            default:
                return 'grey';
        }
    };

    return (
        <div className="view-offer-details-container">
            <SidebarMenu /> {/* Add the SidebarMenu component */}
            <div className="header">
                <h2>Detalles de la oferta</h2>
            </div>
            <div className="details-container">
                <h3>Datos del cliente</h3>
                <div className="client-details">
                    <div>
                        <p><strong>Nombre:</strong> <span className="client-name">{offer.nombre_cliente}</span></p>
                        <p><strong>Semáforo:</strong> {offer.semaforo}</p>
                        <p><strong>Suma asegurada:</strong> {offer.suma_asegurada} €</p>
                        <p><strong>Límite por anualidad:</strong> {offer.limite_anualidad} €</p>
                    </div>
                    <div className="semaforo-container">
                        <div className="semaforo-circle" style={{ backgroundColor: 'black' }}>
                            <div className="semaforo-circle-inner" style={{ backgroundColor: getSemaforoColor(offer.semaforo) }}></div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="coverages-container">
                <h3>Coberturas</h3>
                <ul>
                    {offer.coberturas.map((coverage, index) => (
                        <li key={index}>
                            <p><strong>{coverage.nombre_cobertura}</strong></p>
                            <p>Franquicia: {coverage.franquicia === 'Sin franquicia' ? coverage.franquicia : `${coverage.franquicia} €`}</p>
                            <p>Sublimite: {coverage.sublimite} €</p>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default ViewOfferDetails;
