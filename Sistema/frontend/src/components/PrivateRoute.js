import React, { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { AuthContext } from './AuthContext';

const PrivateRoute = () => {
  const { user } = useContext(AuthContext);

  console.log('PrivateRoute user:', user);

  return user ? <Outlet /> : <Navigate to="/login" />;
};

export default PrivateRoute;
