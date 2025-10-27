import React, { useEffect, useState } from 'react';
import { fetchProjects } from './api';
import './responsive.css';

const App = () => {
  const [repositories, setRepositories] = useState([]);
  const [formData, setFormData] = useState({ owner: '', repo: '' });
  const [status, setStatus] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const loadProjects = async () => {
    try {
      const data = await fetchProjects();
      setRepositories(data.projects || data);
    } catch (error) {
      console.error('Error loading projects:', error);
    }
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setStatus('Importing...');

    try {
      const response = await fetch(`/api/github/save/${formData.owner}/${formData.repo}/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || '',
        },
      });

      const result = await response.json();
      if (response.ok) {
        setStatus('Success!');
      } else {
        setStatus(result.error === 'Repository not found' ? 'Repository not found' : result.error || 'Error occurred');
      }
      if (response.ok) {
        setFormData({ owner: '', repo: '' });
        loadProjects();
      }
    } catch (error) {
      setStatus('Network error');
    } finally {
      setIsLoading(false);
    }
  };

  const totalStars = repositories.reduce((total, repo) => total + repo.stars, 0);
  const uniqueLanguages = new Set(repositories.map(repo => repo.language)).size;

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
        {status && <div className={`message ${status.includes('Success') ? 'success' : 'error'}`}>{status}</div>}
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
              {repositories.slice(0, 10).map((repo) => (
                <tr key={repo.id}>
                  <td>
                    <strong>{repo.name}</strong>
                    <br />
                    <small>{repo.description?.substring(0, 50)}...</small>
                  </td>
                  <td>
                    <span className="tag">{repo.language || 'N/A'}</span>
                  </td>
                  <td>⭐ {repo.stars?.toLocaleString()}</td>
                  <td>{new Date(repo.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default App;