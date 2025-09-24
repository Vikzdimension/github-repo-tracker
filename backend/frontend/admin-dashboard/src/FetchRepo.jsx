import React, { useState } from 'react';

// Helper function to get CSRF from cookies
const getCsrfToken = () => {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    if (name === 'csrftoken') {
      return decodeURIComponent(value);
    }
  }
  return null;
};

const FetchRepo = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    owner: '',
    repo: ''
  });
  const [status, setStatus] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setStatus('Importing repository...');

    const csrfToken = getCsrfToken();
    const { owner, repo } = formData;

    try {
      const response = await fetch(`/api/github/save/${owner}/${repo}/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
      });

      const result = await response.json();

      if (response.ok) {
        setStatus(result.message || 'Repository imported successfully!');
        setFormData({ owner: '', repo: '' });
        if (onSuccess) {
          onSuccess();
        }
      } else {
        setStatus(result.error || 'Failed to import repository');
      }
    } catch (error) {
      setStatus('Network error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="github-form">
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <label htmlFor="owner">Repository Owner</label>
          <input
            id="owner"
            name="owner"
            type="text"
            placeholder="e.g., facebook"
            value={formData.owner}
            onChange={handleInputChange}
            disabled={isLoading}
            required
          />
        </div>
        <div className="form-row">
          <label htmlFor="repo">Repository Name</label>
          <input
            id="repo"
            name="repo"
            type="text"
            placeholder="e.g., react"
            value={formData.repo}
            onChange={handleInputChange}
            disabled={isLoading}
            required
          />
        </div>
        <button 
          type="submit" 
          className="btn-primary"
          disabled={isLoading}
        >
          {isLoading ? 'Importing...' : 'Import Repository'}
        </button>
      </form>
      
      {status && (
        <div className={`message ${status.includes('success') ? 'success' : 'error'}`}>
          {status}
        </div>
      )}
    </div>
  );
};

export default FetchRepo;