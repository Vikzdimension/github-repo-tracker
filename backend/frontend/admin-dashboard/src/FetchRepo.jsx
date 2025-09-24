import { useState } from "react";


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function FetchRepo({ onSuccess }) {

  const [owner, setOwner] = useState("");
  const [repo, setRepo] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("Fetching...");

    try {
            const res = await fetch(`http://127.0.0.1:8000/api/github/save/${owner}/${repo}/`, {
                method: "POST",
                credentials: "include",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            });
            const data = await res.json();

            if (!res.ok) {
                setMessage(data.error || "Error fetching repo");
            } else {
                setMessage(data.message || "Repo saved successfully");
                if (onSuccess) onSuccess();
            }
    } catch (err) {
      setMessage("Network error");
    }
  };

  return (
    <div>
      <h2>Fetch & Save GitHub Repo</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Owner"
          value={owner}
          onChange={(e) => setOwner(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Repo"
          value={repo}
          onChange={(e) => setRepo(e.target.value)}
          required
        />
        <button type="submit">Fetch & Save</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default FetchRepo