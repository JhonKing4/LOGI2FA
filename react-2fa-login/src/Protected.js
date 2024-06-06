import React, { useEffect, useState } from 'react';
import axios from 'axios';
import "./TwoFactor"

const Protected = () => {
    const [message, setMessage] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/protected');
                setMessage(response.data.message);
            } catch (error) {
                setMessage(error.response.data.message);
            }
        };
        fetchData();
    }, []);

    return (
        <div>
            <h2>Hola al Inicio</h2>
            {message && <p>Bienvenido</p>}
        </div>
    );
};

export default Protected;
