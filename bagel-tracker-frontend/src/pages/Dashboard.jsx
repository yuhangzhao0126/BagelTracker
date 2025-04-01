import './Dashboard.css';
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { isAuthenticated, logout } from '../services/authService';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is authenticated
    if (!isAuthenticated()) {
      navigate('/login');
      return;
    }

    // Get user data from localStorage
    const userData = localStorage.getItem('user');
    if (userData) {
      try {
        setUser(JSON.parse(userData));
      } catch (error) {
        console.error('Error parsing user data:', error);
      }
    }
  }, [navigate]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-8">
          <div className="card shadow-sm">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center mb-4">
                <h2 className="card-title text-primary mb-0">
                  {user ? `Hi ${user.name}! 👋` : 'Welcome to your Dashboard'}
                </h2>
                <button 
                  className="btn btn-outline-danger" 
                  onClick={handleLogout}
                >
                  Logout
                </button>
              </div>
              <p className="card-text">
                This is your personal dashboard. Here you can manage your account and access all features.
              </p>
              {/* Add more dashboard content here */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;