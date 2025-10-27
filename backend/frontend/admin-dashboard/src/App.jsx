import React, { useEffect, useState, useCallback } from 'react';
import { fetchProjects } from './api';
import './admin-styles.css';

const App = () => {
  const [repositories, setRepositories] = useState([]);
  const [formData, setFormData] = useState({ owner: '', repo: '' });
  const [status, setStatus] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadProjects = useCallback(async () => {
    try {
      setError(null);
      const data = await fetchProjects();
      setRepositories(data.projects || data);
    } catch (error) {
      console.error('Error loading projects:', error);
      setError('Failed to load projects');
    }
  }, []);

  useEffect(() => {
    loadProjects();
  }, []);

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    if (!formData.owner.trim() || !formData.repo.trim()) {
      setStatus('Please enter both owner and repository name');
      return;
    }

    setIsLoading(true);
    setStatus('Importing...');
    setError(null);

    try {
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                       document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='))?.split('=')[1];
      
      const response = await fetch(`/api/github/save/${encodeURIComponent(formData.owner)}/${encodeURIComponent(formData.repo)}/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken || '',
        },
      });

      const result = await response.json();
      if (response.ok) {
        setStatus('Repository imported successfully!');
        setFormData({ owner: '', repo: '' });
        await loadProjects();
      } else {
        setStatus(result.error || 'Failed to import repository');
      }
    } catch (error) {
      console.error('Import error:', error);
      setStatus('Network error occurred');
    } finally {
      setIsLoading(false);
    }
  }, [formData, loadProjects]);

  const totalStars = repositories.reduce((total, repo) => total + (repo.stars || 0), 0);
  const uniqueLanguages = new Set(repositories.map(repo => repo.language).filter(Boolean)).size;

  return (
    <div className="dashboard">
      <div className="card">
        <h3>Import GitHub Repository</h3>
        <form onSubmit={handleSubmit} className="form">
          <input
            type="text"
            placeholder="Owner (e.g., facebook)"
            value={formData.owner}
            onChange={(e) => setFormData({...formData, owner: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Repository (e.g., react)"
            value={formData.repo}
            onChange={(e) => setFormData({...formData, repo: e.target.value})}
            required
          />
          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Importing...' : 'Import'}
          </button>
        </form>
        {status && (
          <div className={`message ${status.includes('success') || status.includes('Success') ? 'success' : 'error'}`}>
            {status}
          </div>
        )}
        {error && <div className="message error">{error}</div>}
      </div>

      <div className="card">
        <h3>Statistics</h3>
        <div className="stats">
          <div className="stat">
            <span className="number">{repositories.length}</span>
            <span className="label">Repositories</span>
          </div>
          <div className="stat">
            <span className="number">{totalStars.toLocaleString()}</span>
            <span className="label">Total Stars</span>
          </div>
          <div className="stat">
            <span className="number">{uniqueLanguages}</span>
            <span className="label">Languages</span>
          </div>
        </div>
      </div>

      <div className="card">
        <h3>Recent Repositories</h3>
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Repository</th>
                <th>Language</th>
                <th>Stars</th>
                <th>Added</th>
              </tr>
            </thead>
            <tbody>
              {repositories.length === 0 ? (
                <tr>
                  <td colSpan="4" style={{ textAlign: 'center', padding: '20px', color: '#666' }}>
                    No repositories found. Import your first repository above.
                  </td>
                </tr>
              ) : (
                repositories.slice(0, 10).map((repo) => (
                  <tr key={repo.id}>
                    <td>
                      <strong>{repo.name}</strong>
                      {repo.description && (
                        <>
                          <br />
                          <small>{repo.description.substring(0, 50)}{repo.description.length > 50 ? '...' : ''}</small>
                        </>
                      )}
                    </td>
                    <td>
                      <span className="tag">{repo.language || 'N/A'}</span>
                    </td>
                    <td>⭐ {(repo.stars || 0).toLocaleString()}</td>
                    <td>{new Date(repo.created_at).toLocaleDateString()}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default App;