import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Select from 'react-select';
import SidebarMenu from './SidebarMenu'; // Import the SidebarMenu component
import '../styles/CreateOffer.css'; // Import the CSS file

const CreateOffer = () => {
  const [activities, setActivities] = useState([]);
  const [provinces, setProvinces] = useState([]);
  const [selectedActivityIds, setSelectedActivityIds] = useState([]);
  const [selectedProvince, setSelectedProvince] = useState('');
  const [formData, setFormData] = useState({
    id_cliente: '',
    nombre_cliente: '',
    volumen_facturacion: '',
    provincia: '',
    actividades: []
  });
  const [message, setMessage] = useState('');
  const [messageColor, setMessageColor] = useState('');  
  const [createdOfferId, setCreatedOfferId] = useState(null);  // Estado para almacenar el ID de la oferta creada
  const navigate = useNavigate();

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/actividades/');
        setActivities(response.data);
      }
      catch (error) {
        console.error('Error fetching activities:', error);
      }
    };

    const fetchProvinces = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/provincias/');
        setProvinces(response.data);
      } catch (error) {
        console.error('Error fetching provinces:', error);
      }
    };

    fetchActivities();
    fetchProvinces();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleActivityChange = (selectedOptions) => {
    const selectedActivityIds = selectedOptions.map(option => option.value);
    setSelectedActivityIds(selectedActivityIds);
    setFormData({ ...formData, actividades: selectedActivityIds });
  };

  const handleProvinceChange = (e) => {
    setSelectedProvince(e.target.value);
    setFormData({ ...formData, provincia: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const dataToSend = {
      ...formData,
      volumen_facturacion: parseFloat(formData.volumen_facturacion),  
      actividades: selectedActivityIds  
    };
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/crear_oferta_completa/', dataToSend);
      setMessage('Oferta creada exitosamente. Pulsa para ver el resultado');
      setMessageColor('green');
      setCreatedOfferId(response.data.oferta_id);  // Almacenar el ID de la oferta creada
      console.log('Oferta creada exitosamente:', response.data);
    } catch (error) {
      setMessage('Error creando la oferta');
      setMessageColor('red');
      console.error('Error creating offer:', error);
    }
  };

  const handleMessageClick = () => {
    if (messageColor === 'green' && createdOfferId) {
      navigate(`/view-offer-details/${createdOfferId}`);
    }
  };

  const capitalizeWords = (str) => {
    return str.replace(/\b\w/g, char => char.toUpperCase());
  };

  const activityOptions = activities.map(activity => ({
    value: activity.id_actividad,
    label: activity.nombre_actividad
  }));

  return (
    <div className="create-offer-container">
      <SidebarMenu /> {/* Add the SidebarMenu component */}
      <div className="header">
        <h2>Crear oferta</h2>
      </div>
      <form className="create-offer-form" onSubmit={handleSubmit}>
        <div>
          <label>CIF/DNI:</label>
          <input
            type="text"
            name="id_cliente"
            value={formData.id_cliente}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label>Nombre:</label>
          <input
            type="text"
            name="nombre_cliente"
            value={formData.nombre_cliente}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label>Volumen de Facturación:</label>
          <input
            type="text"
            name="volumen_facturacion"
            value={formData.volumen_facturacion}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label>Provincia:</label>
          <select value={selectedProvince} onChange={handleProvinceChange}>
            <option value="" disabled>Seleccionar provincia</option>
            {provinces.map((province) => (
              <option key={province.nombre_provincia} value={province.nombre_provincia}>
                {capitalizeWords(province.nombre_provincia)}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Actividades:</label>
          <Select
            isMulti
            options={activityOptions}
            value={activityOptions.filter(option => selectedActivityIds.includes(option.value))}
            onChange={handleActivityChange}
            placeholder="Seleccionar actividad"
            className="activity-select"
            classNamePrefix="select"
          />
        </div>
        <button type="submit">Crear oferta</button>
      </form>
      {message && <p className="message" style={{ color: messageColor, cursor: messageColor === 'green' ? 'pointer' : 'default' }} onClick={handleMessageClick}>{message}</p>}
    </div>
  );
};

export default CreateOffer;
