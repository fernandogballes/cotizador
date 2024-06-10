import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './components/AuthContext';
import MainMenu from './components/MainMenu';
import CreateOffer from './components/CreateOffer';
import ViewOffers from './components/ViewOffers';
import ViewOfferDetails from './components/ViewOfferDetails';
import Login from './components/Login';
import Register from './components/Register';
import PrivateRoute from './components/PrivateRoute';
import Inicio from './components/Inicio';

const App = () => {
  useEffect(() => {
    // Limpiar tokens de autenticación residuales al iniciar la aplicación
    localStorage.removeItem('authTokens');
  }, []);

  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<Inicio />} />
          <Route path="/" element={<PrivateRoute />}>
            <Route path="menu" element={<MainMenu />} />
            <Route path="create-offer" element={<CreateOffer />} />
            <Route path="view-offers" element={<ViewOffers />} />
            <Route path="view-offer-details/:id" element={<ViewOfferDetails />} />
          </Route>
        </Routes>
      </AuthProvider>
    </Router>
  );
};

export default App;
