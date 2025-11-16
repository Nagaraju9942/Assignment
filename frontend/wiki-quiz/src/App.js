import { useState, useEffect } from "react";
import axios from "axios";
import Modal from "react-modal";

function App() {
  const [url, setUrl] = useState("");
  const [quiz, setQuiz] = useState(null);
  const [history, setHistory] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedQuiz, setSelectedQuiz] = useState(null);

  const generateQuiz = async () => {
    const res = await axios.post("http://localhost:8000/generate_quiz", { url });
    setQuiz(res.data);
  };

  const fetchHistory = async () => {
    const res = await axios.get("http://localhost:8000/history");
    setHistory(res.data);
  };

  useEffect(() => { fetchHistory(); }, []);

  return (
    <div className="container">
      <h1>Wikipedia Quiz Generator</h1>
      <div>
        <input value={url} onChange={(e) => setUrl(e.target.value)} placeholder="Wikipedia URL" />
        <button onClick={generateQuiz}>Generate Quiz</button>
      </div>

      {quiz && (
        <div>
          <h2>{quiz.title}</h2>
          <p>{quiz.summary}</p>
          <h3>Quiz</h3>
          {quiz.quiz.map((q, i) => (
            <div key={i} className="card">
              <strong>{q.question}</strong>
              <ul>
                {q.options.map((o, idx) => <li key={idx}>{o}</li>)}
              </ul>
              <p>Answer: {q.answer}</p>
              <p>Difficulty: {q.difficulty}</p>
              <p>{q.explanation}</p>
            </div>
          ))}
        </div>
      )}

      <h2>History</h2>
      <table>
        <thead>
          <tr>
            <th>URL</th><th>Title</th><th>Details</th>
          </tr>
        </thead>
        <tbody>
          {history.map(h => (
            <tr key={h.id}>
              <td>{h.url}</td>
              <td>{h.title}</td>
              <td><button onClick={() => { setSelectedQuiz(h); setModalOpen(true); }}>Details</button></td>
            </tr>
          ))}
        </tbody>
      </table>

      <Modal isOpen={modalOpen} onRequestClose={() => setModalOpen(false)}>
        {selectedQuiz && (
          <div>
            <h2>{selectedQuiz.title}</h2>
            {selectedQuiz.quiz.map((q, i) => (
              <div key={i}>
                <strong>{q.question}</strong>
                <ul>{q.options.map((o, idx) => <li key={idx}>{o}</li>)}</ul>
                <p>Answer: {q.answer}</p>
              </div>
            ))}
          </div>
        )}
      </Modal>
    </div>
  );
}

export default App;
