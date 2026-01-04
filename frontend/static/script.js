async function sendQuery() {
    const questionInput = document.getElementById("question");
    const responseDiv = document.getElementById("response");

    const question = questionInput.value.trim();

    if (!question) {
        responseDiv.innerHTML = "⚠️ Please enter a question.";
        return;
    }

    responseDiv.innerHTML = "⏳ Thinking...";

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question: question })
        });

        const data = await res.json();

        responseDiv.innerHTML = `
            <p><b>Answer:</b> ${data.answer}</p>
            <p><b>Confidence:</b> ${data.confidence}</p>
            ${data.escalate ? "<p class='escalate'>🚨 Escalated to human agent</p>" : ""}
        `;
    } catch (error) {
        console.error(error);
        responseDiv.innerHTML = "❌ Unable to connect to backend.";
    }
}
