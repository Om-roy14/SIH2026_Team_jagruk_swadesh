import express from "express";
import cors from "cors";

const app = express();

const port = 3000;
const RAG_URL = "http://127.0.0.1:5000";

app.use(cors());
app.use(express.json());

app.get("/api/health", async (req, res) => {
    try {
        const response = await fetch(
            `${RAG_URL}/health`
        );
        const data = await response.json();
        res.json(data);
    } catch (error) {
        res.json({
            ready: false
        });
    }
});

app.post("/api/chat", async (req, res) => {
    try {
        const { question } = req.body;
        if (!question) {
            return res.status(400).json({
                success: false,
                message: "Question is required"
            });
        }
        const response = await fetch(
            `${RAG_URL}/ask`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question
                })
            }
        );
        const data = await response.json();
        res.json(data);
    } catch (error) {
        console.error(error);
        res.status(500).json({
            success: false,
            message: "RAG server unavailable"
        });
    }
});


app.listen(port, () => {
    console.log(
        `Express server running on http://localhost:${port}`
    );

});