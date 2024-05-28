import React, { createContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import jwtDecode from 'jwt-decode';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null);
  const [user, setUser] = useState(() => localStorage.getItem('authTokens') ? jwtDecode(localStorage.getItem('authTokens')) : null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const loginUser = async (username, password) => {
    const response = await axios.post('http://127.0.0.1:8000/api/token/', {
      username,
      password,
    });
    if (response.data) {
      setAuthTokens(response.data);
      setUser(jwtDecode(response.data.access));
      localStorage.setItem('authTokens', JSON.stringify(response.data));
      navigate('/');
    }
  };

  const logoutUser = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem('authTokens');
    navigate('/login');
  };

  useEffect(() => {
    console.log('AuthContext initialized');
    if (authTokens) {
      setUser(jwtDecode(authTokens.access));
      console.log('User authenticated:', jwtDecode(authTokens.access));
    } else {
      console.log('No auth tokens found');
    }
    setLoading(false);
  }, [authTokens]);

  return (
    <AuthContext.Provider value={{ user, loginUser, logoutUser, authTokens }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export { AuthContext };
