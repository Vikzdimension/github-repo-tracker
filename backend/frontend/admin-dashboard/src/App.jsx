import React, { useEffect, useState } from 'react';
import { fetchProjects } from './api';
import FetchRepo from './FetchRepo';
import './admin-styles.css';

const App = () => {
  const [repositories, setRepositories] = useState([]);

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

  const totalStars = repositories.reduce((total, repo) => total + repo.stars, 0);
  const uniqueLanguages = new Set(repositories.map(repo => repo.language)).size;

  return (
    <div className="admin-dashboard" style={{ background: 'transparent', padding: 0, margin: 0 }}>
      <div className="module">
        <h2>Import GitHub Repository</h2>
        <FetchRepo onSuccess={loadProjects} />
      </div>

      <div className="module">
        <h2>Repository Statistics</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <h3>{repositories.length}</h3>
            <p>Total Repositories</p>
          </div>
          <div className="stat-card">
            <h3>{totalStars}</h3>
            <p>Total Stars</p>
          </div>
          <div className="stat-card">
            <h3>{uniqueLanguages}</h3>
            <p>Languages</p>
          </div>
        </div>
      </div>

      <div className="module">
        <h2>Recent Repositories</h2>
        <div className="results">
          <table className="admin-table">
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
                    <small>{repo.description}</small>
                  </td>
                  <td>
                    <span className="language-tag">{repo.language || 'N/A'}</span>
                  </td>
                  <td>⭐ {repo.stars}</td>
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
