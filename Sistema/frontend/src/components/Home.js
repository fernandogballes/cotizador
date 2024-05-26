import React, { useContext } from 'react';
import { AuthContext } from './AuthContext';

const Home = () => {
    const { user, logoutUser } = useContext(AuthContext);

    return (
        <div>
            <h2>Welcome {user && user.username}</h2>
            <button onClick={logoutUser}>Logout</button>
        </div>
    );
};

export default Home;
