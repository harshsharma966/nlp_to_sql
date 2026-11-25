import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://localhost:8032";

// Sample questions for users to try
const SAMPLE_QUESTIONS = [
  "Show all employees with their department name and location",
  "Which employee generated the highest total sales amount?",
  "Show each sales record with employee name, department name, product, and amount",
  "What is the total sales revenue generated so far?",
  "What is the average salary of all employees?",
  "Who is the highest paid employee and what is their salary?",
  "List all user tables in my database"
];

export default function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [sqlQuery, setSqlQuery] = useState("");
  const [rows, setRows] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("answer"); // answer, sql, data
  const [backendStatus, setBackendStatus] = useState("checking");
  const [dbStatus, setDbStatus] = useState("unknown");
  const [history, setHistory] = useState(() => {
    const saved = localStorage.getItem("query_history");
    return saved ? JSON.parse(saved) : [];
  });

  // Check backend health on mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch(`${API_URL}/health`);
        const data = await res.json();
        setBackendStatus("connected");
        setDbStatus(data.database);
      } catch (err) {
        setBackendStatus("disconnected");
        setDbStatus("unknown");
      }
    };
    checkHealth();
  }, []);

  // save history in localStorage
  useEffect(() => {
    localStorage.setItem("query_history", JSON.stringify(history));
  }, [history]);

  const handleSubmit = async (customQuery) => {
    const finalQuery = (customQuery ?? query).trim();
    if (!finalQuery) return;

    // Store in history
    setHistory((prev) => {
      const updated = [finalQuery, ...prev.filter((q) => q !== finalQuery)];
      return updated.slice(0, 15);
    });

    setQuery(finalQuery);
    setAnswer("");
    setSqlQuery("");
    setRows([]);
    setIsLoading(true);
    setActiveTab("answer");

    try {
      const res = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: finalQuery }),
      });

      const data = await res.json();

      setAnswer(data.answer || "No answer received");
      setSqlQuery(data.sql || "");
      setRows(data.rows || []);
    } catch (err) {
      setAnswer("Error connecting to backend. Check if backend is running.");
      setSqlQuery("");
      setRows([]);
    } finally {
      setIsLoading(false);
    }
  };


  const clearHistory = () => {
    setHistory([]);
    localStorage.removeItem("query_history");
  };

  return (
    <div className="layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <h2 className="sideTitle">Universal NLP-to-SQL</h2>

        {/* Backend Status Indicator */}
        <div className="statusIndicator">
          <span className={`statusDot ${backendStatus}`}></span>
          <span className="statusText">
            {backendStatus === "checking" && "Checking backend..."}
            {backendStatus === "connected" && `Backend: OK | DB: ${dbStatus}`}
            {backendStatus === "disconnected" && "Backend: Offline"}
          </span>
        </div>

        <p className="sideSub">Recent Queries</p>

        <div className="historyList">
          {history.length === 0 ? (
            <div className="empty">No previous queries</div>
          ) : (
            history.map((q, i) => (
              <button
                key={i}
                className="historyItem"
                onClick={() => handleSubmit(q)}
              >
                {q}
              </button>
            ))
          )}
        </div>

        <button className="clearBtn" onClick={clearHistory}>
          Clear
        </button>
      </aside>

      {/* Main */}
      <main className="page">
        <div className="card">
          <h1 className="title">Universal NLP-to-SQL AI</h1>
          <p className="subtitle">
            Ask database questions in Natural Language (PostgreSQL, MySQL, SQLite powered by Ollama).
          </p>

          <div className="inputRow">
            <input
              className="input"
              placeholder="e.g. Show all employees with their department name and location"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
              disabled={isLoading}
            />
            <button className="btn" onClick={() => handleSubmit()} disabled={isLoading}>
              {isLoading ? "Loading..." : "Ask"}
            </button>
          </div>

          {/* Sample Questions */}
          <div className="sampleQuestions">
            <p className="sampleTitle">Try these questions:</p>
            <div className="sampleList">
              {SAMPLE_QUESTIONS.map((q, i) => (
                <button
                  key={i}
                  className="sampleBtn"
                  onClick={() => handleSubmit(q)}
                  disabled={isLoading}
                >
                  {q}
                </button>
              ))}
            </div>
          </div>

          {/* Results Section */}
          {(answer || isLoading) && (
            <div className="results">
              {/* Tabs */}
              <div className="tabs">
                <button
                  className={`tab ${activeTab === "answer" ? "active" : ""}`}
                  onClick={() => setActiveTab("answer")}
                >
                  Answer
                </button>
                <button
                  className={`tab ${activeTab === "sql" ? "active" : ""}`}
                  onClick={() => setActiveTab("sql")}
                >
                  SQL Query
                </button>
                <button
                  className={`tab ${activeTab === "data" ? "active" : ""}`}
                  onClick={() => setActiveTab("data")}
                >
                  Data ({rows.length} rows)
                </button>
              </div>

              {/* Tab Content */}
              <div className="tabContent">
                {isLoading ? (
                  <div className="loading">Processing your query...</div>
                ) : (
                  <>
                    {activeTab === "answer" && (
                      <div className="answerBox">
                        <pre>{answer}</pre>
                      </div>
                    )}

                    {activeTab === "sql" && (
                      <div className="sqlBox">
                        <code>{sqlQuery || "No SQL generated"}</code>
                      </div>
                    )}

                    {activeTab === "data" && (
                      <div className="dataBox">
                        {rows.length > 0 ? (
                          <div className="tableWrapper">
                            <table className="dataTable">
                              <thead>
                                <tr>
                                  {Object.keys(rows[0]).map((key) => (
                                    <th key={key}>{key}</th>
                                  ))}
                                </tr>
                              </thead>
                              <tbody>
                                {rows.slice(0, 50).map((row, i) => (
                                  <tr key={i}>
                                    {Object.values(row).map((val, j) => (
                                      <td key={j}>{val?.toString() ?? "-"}</td>
                                    ))}
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                            {rows.length > 50 && (
                              <p className="moreRows">Showing 50 of {rows.length} rows</p>
                            )}
                          </div>
                        ) : (
                          <p className="noData">No data returned</p>
                        )}
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
