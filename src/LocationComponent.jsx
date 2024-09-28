import React, { useEffect, useState } from 'react';

const LocationComponent = () => {
  const [locationData, setLocationData] = useState(null);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        setLocationData({ latitude, longitude });
      },
      (error) => {
        console.error('Error getting location:', error);
      }
    );
  }, []);

  // ... rest of your component
};