import './Dashboard.css';
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { isAuthenticated, logout } from '../services/authService';
import MatchForm from '../components/MatchForm/MatchForm';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [showMatchForm, setShowMatchForm] = useState(false);
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

  const handleMatchRecorded = (response) => {
    console.log('Match recorded:', response);
    // You could add additional logic here, such as refreshing a list of matches
  };

  const toggleMatchForm = () => {
    setShowMatchForm(!showMatchForm);
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-10">
          <div className="card shadow-sm mb-4">
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
                This is your personal dashboard for BagelTracker. Here you can record tennis matches and track "bagels"!
              </p>
              
              <div className="d-grid mb-4">
                <button
                  className="btn btn-tennis-primary border border-2 border-primary"
                  onClick={toggleMatchForm}
                >
                  {showMatchForm ? 'Hide Match Form' : '🎾 Record a Tennis Match'}
                </button>
              </div>
              
              {showMatchForm && (
                <MatchForm onMatchRecorded={handleMatchRecorded} />
              )}
            </div>
          </div>
          
          {/* Future development: Add match history section here */}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;