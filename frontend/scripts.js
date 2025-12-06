let mediaRecorder;
let audioChunks = [];

// Start Recording
document.getElementById("startBtn").onclick = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    audioChunks = [];
    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        sendToTranscribe(audioBlob);
    };

    mediaRecorder.start();
    console.log("Recording started...");
};

// Stop Recording
document.getElementById("stopBtn").onclick = () => {
    if (mediaRecorder) {
        mediaRecorder.stop();
        console.log("Recording stopped.");
    }
};

// Send audio to backend
async function sendToTranscribe(audioBlob) {
    const formData = new FormData();
    formData.append("audio", audioBlob, "recording.wav");

    const response = await fetch("http://127.0.0.1:5000/transcribe", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    document.getElementById("transcription").innerText = data.text;

    sendTextToChat(data.text);
}

// Send text to AI
async function sendTextToChat(text) {
    const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });

    const data = await response.json();

    document.getElementById("reply").innerText = data.reply;

    // Play AI Audio
    if (data.audio) {
        const audio = new Audio(`http://127.0.0.1:5000/${data.audio}`);
        audio.play();
    }
}
