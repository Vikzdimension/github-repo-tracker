import { useEffect, useState } from "react";
import { fetchProjects } from "./api";
import FetchRepo from "./FetchRepo";

function App() {
  const [projects, setProjects] = useState([]);

  const refreshProjects = () => {

    fetchProjects()
        .then((data) => setProjects(data.projects || data))
        .catch((error) => console.error("Failed to fetch projects:", error));
    };
    useEffect(() => {
      fetchProjects()
        .then((data) => setProjects(data.projects || data))
        .catch((error) => console.error("Failed to fetch projects:", error));
    }, []);

  return (
    <div>
      <h1>Projects Dashboard</h1>
      <FetchRepo onSuccess={refreshProjects} />
      <h2>Existing Projects</h2>
      <ul>
        {projects.map((p) => (
          <li key={p.id}>
            {p.name} - {p.language} - ⭐ {p.stars}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
