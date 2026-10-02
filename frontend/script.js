const API_URL = "";

// LOAD VIDEO
async function loadVideo() {

    const videoLink =
        document.getElementById("videoLink").value.trim();

    const button =
        document.getElementById("loadButton");

    const status =
        document.getElementById("videoStatus");


    // Check URL
    if (videoLink === "") {

        status.className = "message error";

        status.textContent =
            "Please enter a YouTube link.";

        return;
    }


    // Loading state
    button.disabled = true;

    button.innerHTML =
        "<span>Loading...</span>";

    status.className = "message loading";

    status.textContent =
        "Fetching transcript and creating RAG...";


    try {

        const response = await fetch(
            `${API_URL}/load-video`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    video_link: videoLink
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Failed to load video."
            );
        }


        // Success
        status.className =
            "message success";

        status.textContent =
            "✓ Video loaded successfully. You can now ask questions.";

    }

    catch (error) {

        status.className =
            "message error";

        status.textContent =
            "Error: " + error.message;
    }


    finally {

        button.disabled = false;

        button.innerHTML =
            "<span>Load Video</span>";
    }
}


// ASK QUESTION

async function askQuestion() {

    const question =
        document.getElementById("question").value.trim();

    const button =
        document.getElementById("askButton");

    const answerBox =
        document.getElementById("answer");

    const status =
        document.getElementById("questionStatus");


    // Check question
    if (question === "") {

        status.className =
            "message error";

        status.textContent =
            "Please enter a question.";

        return;
    }


    // Loading state
    button.disabled = true;

    button.innerHTML =
        "<span>Thinking...</span>";


    status.className =
        "message loading";

    status.textContent =
        "Searching the transcript...";


    answerBox.innerHTML = `
        <div class="answer-placeholder">
            <div class="bot-icon">✦</div>
            <p>Generating answer...</p>
        </div>
    `;


    try {

        const response = await fetch(
            `${API_URL}/ask`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Failed to generate answer."
            );
        }


        // Display answer
        answerBox.textContent =
            data.answer;


        status.className =
            "message success";

        status.textContent =
            "✓ Answer generated.";


    }

    catch (error) {

        answerBox.textContent =
            "Something went wrong.";

        status.className =
            "message error";

        status.textContent =
            "Error: " + error.message;
    }


    finally {

        button.disabled = false;

        button.innerHTML = `
            <span>Ask Question</span>
            <span class="arrow">→</span>
        `;
    }
}