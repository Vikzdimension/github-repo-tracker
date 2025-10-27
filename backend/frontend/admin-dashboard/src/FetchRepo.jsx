import React, { useState, useEffect } from 'react';
import { useScreenSize } from './ResponsiveUtils';

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
  const { isMobile } = useScreenSize();

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
      <form onSubmit={handleSubmit} style={{ 
        display: 'flex', 
        flexDirection: isMobile ? 'column' : 'row',
        flexWrap: 'wrap',
        gap: 'clamp(10px, 3vw, 15px)',
        alignItems: isMobile ? 'stretch' : 'flex-end'
      }}>
        <div className="form-row" style={{ flex: isMobile ? '1' : '0 1 200px' }}>
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
            autoComplete="off"
            inputMode="text"
          />
        </div>
        <div className="form-row" style={{ flex: isMobile ? '1' : '0 1 200px' }}>
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
            autoComplete="off"
            inputMode="text"
          />
        </div>
        <button 
          type="submit" 
          className="btn-primary"
          disabled={isLoading}
          style={{ 
            opacity: isLoading ? 0.6 : 1,
            cursor: isLoading ? 'not-allowed' : 'pointer',
            flex: isMobile ? '1' : '0 0 auto',
            alignSelf: isMobile ? 'stretch' : 'flex-end'
          }}
        >
          {isLoading ? (
            <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
              <span style={{
                display: 'inline-block',
                width: '16px',
                height: '16px',
                border: '2px solid #ffffff40',
                borderTop: '2px solid #ffffff',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite'
              }}></span>
              Importing...
            </span>
          ) : 'Import Repository'}
        </button>
      </form>
      
      {status && (
        <div 
          className={`message ${status.includes('success') || status.includes('successfully') ? 'success' : 'error'}`}
          role="alert"
          aria-live="polite"
        >
          {status}
        </div>
      )}
      
      <style jsx>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default FetchRepo;