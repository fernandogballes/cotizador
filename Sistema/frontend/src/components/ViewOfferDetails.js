import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

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
        <div>
            <h2>Offer Details</h2>
            <p><strong>Client Name:</strong> {offer.nombre_cliente}</p>
            <p><strong>Sum Insured:</strong> {offer.suma_asegurada}</p>
            <p><strong>Annual Limit:</strong> {offer.limite_anualidad}</p>
            <h3>Coverages</h3>
            <ul>
                {offer.coberturas.map((coverage, index) => (
                    <li key={index}>
                        <p><strong>Coverage Name:</strong> {coverage.nombre_cobertura}</p>
                        <p><strong>Deductible:</strong> {coverage.franquicia}</p>
                        <p><strong>Sub-limit:</strong> {coverage.sublimite}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ViewOfferDetails;
