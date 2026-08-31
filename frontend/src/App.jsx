import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";
import Input from "./input";

function App() {
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        if (!question.trim() || loading) return;

        const userQuestion = question.trim();
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
            <header className="header">
                <div className="logo">
                    BIS AI
                </div>

                <div className="status">
                    <span className="status-dot"></span>
                    BIS Knowledge Assistant
                </div>
            </header>

            <main className="chat-container">

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

                    <Input
            question={question}
            setQuestion={setQuestion}
            handleKeyDown={handleKeyDown}
            loading={loading}
            sendMessage={sendMessage}
                />

        </div>
    );
}

export default App;