import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CreateOffer = () => {
  const [activities, setActivities] = useState([]);
  const [provinces, setProvinces] = useState([]);
  const [selectedActivities, setSelectedActivities] = useState([]);
  const [selectedActivityIds, setSelectedActivityIds] = useState([]);
  const [selectedProvince, setSelectedProvince] = useState('');
  const [formData, setFormData] = useState({
    id_cliente: '',
    nombre_cliente: '',
    volumen_facturacion: '',
    provincia: '',
    actividades: []
  });

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/actividades/');
        setActivities(response.data);
      } catch (error) {
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

  const handleActivityChange = (e) => {
    const selectedActivityId = parseInt(e.target.value);
    if (!selectedActivityIds.includes(selectedActivityId)) {
      const selectedActivityName = activities.find(activity => activity.id_actividad === selectedActivityId).nombre_actividad;
      setSelectedActivities([...selectedActivities, selectedActivityName]);
      setSelectedActivityIds([...selectedActivityIds, selectedActivityId]);
      setFormData({ ...formData, actividades: [...selectedActivityIds, selectedActivityId] });
    }
  };

  const handleProvinceChange = (e) => {
    setSelectedProvince(e.target.value);
    setFormData({ ...formData, provincia: e.target.value });
  };

  const removeActivity = (activity) => {
    const index = selectedActivities.indexOf(activity);
    if (index > -1) {
      const updatedActivities = selectedActivities.filter((_, i) => i !== index);
      const updatedActivityIds = selectedActivityIds.filter((_, i) => i !== index);
      setSelectedActivities(updatedActivities);
      setSelectedActivityIds(updatedActivityIds);
      setFormData({ ...formData, actividades: updatedActivityIds });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const dataToSend = {
      ...formData,
      volumen_facturacion: parseFloat(formData.volumen_facturacion),  // Ensure volume_facturacion is a float
      actividades: selectedActivityIds  // Ensure activities are sent as ids
    };
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/crear_oferta_completa/', dataToSend);
      console.log('Oferta creada exitosamente:', response.data);
    } catch (error) {
      console.error('Error creating offer:', error);
    }
  };

  return (
    <div>
      <h2>Crear Oferta</h2>
      <form onSubmit={handleSubmit}>
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
            {provinces.map((province, index) => (
              <option key={index} value={province.nombre_provincia}>
                {province.nombre_provincia}
              </option>
            ))}
          </select>
        </div>
        {selectedProvince && (
          <div>
            <strong>Provincia seleccionada:</strong> {selectedProvince}
          </div>
        )}
        <div>
          <label>Actividades:</label>
          <select value="" onChange={handleActivityChange}>
            <option value="" disabled>Seleccionar actividad</option>
            {activities.map((activity) => (
              <option key={activity.id_actividad} value={activity.id_actividad}>
                {activity.nombre_actividad}
              </option>
            ))}
          </select>
        </div>
        <div>
          <strong>Actividades seleccionadas:</strong>
          <ul>
            {selectedActivities.map((activity, index) => (
              <li key={index} onClick={() => removeActivity(activity)} style={{ cursor: 'pointer' }}>
                {activity}
              </li>
            ))}
          </ul>
        </div>
        <button type="submit">Crear Oferta</button>
      </form>
    </div>
  );
};

export default CreateOffer;
