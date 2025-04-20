import React, { useState, useEffect } from 'react';
import { searchUsers } from '../../services/apiService';
import './UserSearch.css';

const UserSearch = ({ onSelectUser }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Search users when searchTerm changes with debounce
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (searchTerm.trim()) {
        handleSearch();
      } else {
        setSearchResults([]);
      }
    }, 300); // 300ms delay to avoid too many requests

    return () => clearTimeout(delayDebounceFn);
  }, [searchTerm]);

  const handleSearch = async () => {
    if (!searchTerm.trim()) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await searchUsers(searchTerm);
      if (response.success) {
        setSearchResults(response.users);
      } else {
        setError('Failed to fetch results');
      }
    } catch (error) {
      console.error('Error searching users:', error);
      setError(error.message || 'An error occurred while searching');
    } finally {
      setIsLoading(false);
    }
  };

  const handleUserSelect = (user) => {
    onSelectUser(user);
    setSearchTerm('');
    setSearchResults([]);
  };

  return (
    <div className="user-search-container">
      <h4>Search Users</h4>
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Type a username to search (e.g., 'user')"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          aria-label="Search users"
        />
      </div>
      
      {/* Loading Indicator */}
      {isLoading && (
        <div className="text-center my-3">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      )}
      
      {/* Error Message */}
      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}
      
      {/* Search Results */}
      {searchResults.length > 0 && !isLoading && (
        <div className="list-group search-results">
          {searchResults.map((user) => (
            <button
              key={user.user_id}
              type="button"
              className="list-group-item list-group-item-action"
              onClick={() => handleUserSelect(user)}
            >
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <strong>{user.name}</strong>
                </div>
                <span className="badge bg-primary rounded-pill">Select</span>
              </div>
            </button>
          ))}
        </div>
      )}
      
      {/* No Results Message */}
      {searchTerm && searchResults.length === 0 && !isLoading && !error && (
        <div className="alert alert-info">
          No users found matching "{searchTerm}"
        </div>
      )}
    </div>
  );
};

export default UserSearch;