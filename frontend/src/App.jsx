import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";

function App() {
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        if (!question.trim() || loading) return;

        const userQuestion = question.trim();

        // Add user's message immediately
        setMessages((prev) => [
            ...prev,
            {
                role: "user",
                content: userQuestion,
            },
        ]);

        setQuestion("");
        setLoading(true);

        try {
            const response = await fetch(
                "http://localhost:3000/api/chat",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        question: userQuestion,
                    }),
                }
            );

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(
                    data.message || "Something went wrong"
                );
            }

            // Add AI response
            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content: data.answer,
                },
            ]);
        } catch (error) {
            console.error(error);

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content:
                        "Sorry, I couldn't connect to the BIS AI server.",
                },
            ]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className="app">

            {/* Header */}
            <header className="header">
                <div className="logo">
                    BIS AI
                </div>

                <div className="status">
                    <span className="status-dot"></span>
                    BIS Knowledge Assistant
                </div>
            </header>


            {/* Chat Area */}
            <main className="chat-container">

                {/* Empty screen */}
                {messages.length === 0 && !loading && (
                    <div className="welcome">

                        <div className="welcome-icon">
                            BIS
                        </div>

                        <h1>
                            BIS AI Assistant
                        </h1>

                        <p>
                            Ask questions about BIS standards,
                            certification, laboratories and licences.
                        </p>

                        <div className="suggestions">

                            <button
                                onClick={() =>
                                    setQuestion(
                                        "What is the BIS standard for pressure cookers?"
                                    )
                                }
                            >
                                What is the BIS standard for pressure cookers?
                            </button>

                            <button
                                onClick={() =>
                                    setQuestion(
                                        "Which laboratories can test my pressure cooker?"
                                    )
                                }
                            >
                                Find testing laboratories
                            </button>

                            <button
                                onClick={() =>
                                    setQuestion(
                                        "How do I get BIS certification for a pressure cooker?"
                                    )
                                }
                            >
                                How do I get BIS certification?
                            </button>

                        </div>

                    </div>
                )}


                {/* Messages */}
                <div className="messages">

                    {messages.map((message, index) => (

                        <div
                            className={`message-row ${message.role}`}
                            key={index}
                        >

                            <div className="avatar">
                                {message.role === "user"
                                    ? "You"
                                    : "BIS"}
                            </div>

                            <div className="message-content">

                                {message.role === "assistant" ? (

                                    <div className="markdown">

                                        <ReactMarkdown
                                            remarkPlugins={[remarkGfm]}
                                        >
                                            {message.content}
                                        </ReactMarkdown>

                                    </div>

                                ) : (

                                    <div className="user-message">
                                        {message.content}
                                    </div>

                                )}

                            </div>

                        </div>

                    ))}


                    {/* Loading */}
                    {loading && (

                        <div className="message-row assistant">

                            <div className="avatar">
                                BIS
                            </div>

                            <div className="message-content">

                                <div className="loading-message">

                                    <div className="loading-spinner"></div>

                                    <span>
                                        BIS AI is thinking...
                                    </span>

                                </div>

                            </div>

                        </div>

                    )}

                </div>

            </main>


            {/* Input */}
            <div className="input-area">

                <div className="input-box">

                    <textarea
                        value={question}
                        onChange={(e) =>
                            setQuestion(e.target.value)
                        }
                        onKeyDown={handleKeyDown}
                        placeholder="Ask BIS AI anything..."
                        rows="1"
                        disabled={loading}
                    />

                    <button
                        className="send-button"
                        onClick={sendMessage}
                        disabled={
                            loading ||
                            !question.trim()
                        }
                    >
                        ↑
                    </button>

                </div>

                <p className="input-hint">
                    Press Enter to send · Shift + Enter for a new line
                </p>

            </div>

        </div>
    );
}

export default App;