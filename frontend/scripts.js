console.log("scripts.js loaded ✔️");

let mediaRecorder;
let audioChunks = [];

// Start
document.getElementById("startBtn").onclick = async () => {
    console.log("Start button clicked");
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    audioChunks = [];
    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);

    mediaRecorder.onstop = async () => {
        console.log("Recording stopped, sending audio...");
        const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        sendToTranscribe(audioBlob);
    };

    mediaRecorder.start();
    console.log("Recording started...");
};

// Stop
document.getElementById("stopBtn").onclick = () => {
    console.log("Stop button clicked");
    if (mediaRecorder) mediaRecorder.stop();
};

// Send for transcription
async function sendToTranscribe(audioBlob) {
    const formData = new FormData();
    formData.append("audio", audioBlob, "recording.wav");

    console.log("Sending blob to backend...");

    const response = await fetch("http://127.0.0.1:5000/transcribe", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    console.log("Backend transcription:", data.text);

    document.getElementById("transcription").innerText = data.text;

    sendTextToChat(data.text);
}

// Send text to GPT
async function sendTextToChat(text) {
    console.log("Sending to /chat:", text);

    const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });

    const data = await response.json();
    console.log("AI Reply:", data.reply);

    document.getElementById("reply").innerText = data.reply;
}
