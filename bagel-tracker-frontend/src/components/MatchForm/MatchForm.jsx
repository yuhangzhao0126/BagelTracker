// filepath: /Users/zhaoyuhang/project/BagelTracker/bagel-tracker-frontend/src/components/MatchForm/MatchForm.jsx
import React, { useState, useEffect } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { recordMatch, searchUsers } from '../../services/apiService';
import './MatchForm.css';

// Player Selection Component
const PlayerSelector = ({ label, onSelect, selectedPlayer, required }) => {
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

  const handleSelectPlayer = (player) => {
    onSelect(player);
    setSearchTerm('');
    setSearchResults([]);
  };

  return (
    <div className="player-selector mb-3">
      <label className="form-label">{label} {required && <span className="text-danger">*</span>}</label>
      
      {selectedPlayer ? (
        <div className="selected-player mb-2 p-2 border rounded d-flex justify-content-between align-items-center">
          <span>
            <strong>{selectedPlayer.name}</strong>
          </span>
          <button 
            type="button"
            className="btn btn-sm btn-outline-secondary" 
            onClick={() => onSelect(null)}
          >
            Change
          </button>
        </div>
      ) : (
        <>
          <div className="input-group mb-2">
            <input
              type="text"
              className="form-control"
              placeholder="Search for a player..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && e.preventDefault()}
            />
            <button 
              className="btn btn-outline-primary" 
              type="button"
              onClick={handleSearch}
            >
              Search
            </button>
          </div>
          
          {isLoading && <div className="text-center my-2">Loading...</div>}
          
          {error && <div className="alert alert-danger py-1">{error}</div>}
          
          {searchResults.length > 0 && (
            <div className="search-results list-group">
              {searchResults.map(player => (
                <button
                  key={player.user_id}
                  type="button"
                  className="list-group-item list-group-item-action"
                  onClick={() => handleSelectPlayer(player)}
                >
                  {player.name}
                </button>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
};

// Validation Schema
const MatchFormSchema = Yup.object().shape({
  match_type: Yup.string()
    .required('Match type is required')
    .oneOf(['singles', 'doubles'], 'Match type must be singles or doubles'),
  team1_score: Yup.number()
    .required('Team 1 score is required')
    .min(0, 'Score cannot be negative')
    .max(7, 'Score should not exceed 7'),
  team2_score: Yup.number()
    .required('Team 2 score is required')
    .min(0, 'Score cannot be negative')
    .max(7, 'Score should not exceed 7')
});

const MatchForm = ({ onMatchRecorded }) => {
  const [team1Player1, setTeam1Player1] = useState(null);
  const [team1Player2, setTeam1Player2] = useState(null);
  const [team2Player1, setTeam2Player1] = useState(null);
  const [team2Player2, setTeam2Player2] = useState(null);
  const [matchType, setMatchType] = useState('singles');
  const [submitError, setSubmitError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  const handleSubmit = async (values, { resetForm }) => {
    // Validate player selections
    if (!team1Player1 || !team2Player1) {
      setSubmitError('Please select players for both teams');
      return;
    }

    if (matchType === 'doubles' && (!team1Player2 || !team2Player2)) {
      setSubmitError('Please select two players for each team in doubles');
      return;
    }

    // Prepare match data
    const matchData = {
      match_type: matchType,
      team1_player1_id: team1Player1.user_id,
      team1_player2_id: matchType === 'doubles' ? team1Player2.user_id : null,
      team2_player1_id: team2Player1.user_id,
      team2_player2_id: matchType === 'doubles' ? team2Player2.user_id : null,
      team1_score: parseInt(values.team1_score),
      team2_score: parseInt(values.team2_score)
    };

    setIsSubmitting(true);
    setSubmitError(null);

    try {
      const response = await recordMatch(matchData);
      
      if (response.success) {
        // Reset form on success
        resetForm();
        setTeam1Player1(null);
        setTeam1Player2(null);
        setTeam2Player1(null);
        setTeam2Player2(null);
        setShowSuccess(true);
        setTimeout(() => setShowSuccess(false), 5000);
        
        // Call callback if provided
        if (onMatchRecorded) {
          onMatchRecorded(response);
        }
      } else {
        setSubmitError(response.message || 'Failed to record match');
      }
    } catch (error) {
      setSubmitError(error.message || 'An error occurred while recording the match');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="match-form-container">
      <h3 className="mb-4">Record Tennis Match</h3>
      
      {submitError && (
        <div className="alert alert-danger" role="alert">
          {submitError}
        </div>
      )}
      
      {showSuccess && (
        <div className="alert alert-success" role="alert">
          Match recorded successfully!
          {showSuccess.is_bagel && (
            <div className="mt-2">
              <strong>🥯 BAGEL ALERT! 🥯</strong> This match was a bagel!
            </div>
          )}
        </div>
      )}
      
      <div className="mb-4">
        <label className="form-label d-block">Match Type</label>
        <div className="btn-group" role="group">
          <button 
            type="button" 
            className={`btn ${matchType === 'singles' ? 'btn-primary' : 'btn-outline-primary'}`}
            onClick={() => setMatchType('singles')}
          >
            Singles
          </button>
          <button 
            type="button" 
            className={`btn ${matchType === 'doubles' ? 'btn-primary' : 'btn-outline-primary'}`}
            onClick={() => setMatchType('doubles')}
          >
            Doubles
          </button>
        </div>
      </div>
      
      <div className="row">
        <div className="col-md-6">
          <div className="team-container p-3 border rounded mb-4">
            <h4 className="mb-3">Team 1</h4>
            <PlayerSelector 
              label="Player 1"
              selectedPlayer={team1Player1}
              onSelect={setTeam1Player1}
              required={true}
            />
            
            {matchType === 'doubles' && (
              <PlayerSelector 
                label="Player 2"
                selectedPlayer={team1Player2}
                onSelect={setTeam1Player2}
                required={true}
              />
            )}
          </div>
        </div>
        
        <div className="col-md-6">
          <div className="team-container p-3 border rounded mb-4">
            <h4 className="mb-3">Team 2</h4>
            <PlayerSelector 
              label="Player 1"
              selectedPlayer={team2Player1}
              onSelect={setTeam2Player1}
              required={true}
            />
            
            {matchType === 'doubles' && (
              <PlayerSelector 
                label="Player 2"
                selectedPlayer={team2Player2}
                onSelect={setTeam2Player2}
                required={true}
              />
            )}
          </div>
        </div>
      </div>
      
      <Formik
        initialValues={{
          match_type: matchType,
          team1_score: '',
          team2_score: ''
        }}
        validationSchema={MatchFormSchema}
        onSubmit={handleSubmit}
        enableReinitialize
      >
        {({ errors, touched }) => (
          <Form>
            <div className="row">
              <div className="col-md-6">
                <div className="mb-3">
                  <label htmlFor="team1_score" className="form-label">Team 1 Score</label>
                  <Field
                    name="team1_score"
                    type="number"
                    className={`form-control ${errors.team1_score && touched.team1_score ? 'is-invalid' : ''}`}
                    min="0"
                    max="7"
                  />
                  <ErrorMessage name="team1_score" component="div" className="invalid-feedback" />
                </div>
              </div>
              
              <div className="col-md-6">
                <div className="mb-3">
                  <label htmlFor="team2_score" className="form-label">Team 2 Score</label>
                  <Field
                    name="team2_score"
                    type="number"
                    className={`form-control ${errors.team2_score && touched.team2_score ? 'is-invalid' : ''}`}
                    min="0"
                    max="7"
                  />
                  <ErrorMessage name="team2_score" component="div" className="invalid-feedback" />
                </div>
              </div>
            </div>
            
            <div className="d-grid gap-2">
              <button
                type="submit"
                className="btn btn-success btn-lg"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Recording...' : 'Record Match'}
              </button>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default MatchForm;