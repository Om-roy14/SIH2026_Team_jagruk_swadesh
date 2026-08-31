import React from "react";

function Input({
    question,
    setQuestion,
    handleKeyDown,
    loading,
    sendMessage
}) {
    return (
        <div className="input-area">

            <div className="input-box">

                <textarea
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask BIS AI anything..."
                    rows="1"
                    disabled={loading}
                />

                <button
                    className="send-button"
                    onClick={sendMessage}
                    disabled={loading || !question.trim()}
                >
                    ↑
                </button>

            </div>

            <p className="input-hint">
                Press Enter to send · Shift + Enter for a new line
            </p>

        </div>
    );
}

export default Input;