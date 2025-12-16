let recorder;
let audioChunks = [];
let isRecording = false;

const recordBtn = document.getElementById("recordBtn");
const result = document.getElementById("result");
const micCircle = document.getElementById("micCircle");

recordBtn.onclick = async () => {
    if (!isRecording) {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        recorder = new MediaRecorder(stream);
        recorder.start();

        audioChunks = [];
        recorder.ondataavailable = e => audioChunks.push(e.data);

        micCircle.classList.add("active");
        recordBtn.textContent = "Stop Speaking";
        recordBtn.classList.add("recording");
        isRecording = true;

    } else {
        recorder.stop();
        micCircle.classList.remove("active");
        recordBtn.textContent = "Start Speaking";
        recordBtn.classList.remove("recording");
        isRecording = false;

        recorder.onstop = async () => {
            const blob = new Blob(audioChunks, { type: "audio/wav" });
            const formData = new FormData();
            formData.append("audio", blob);

            result.textContent = "Translating...";

            const response = await fetch("/translate", {
                method: "POST",
                body: formData
            });

            const data = await response.json();
            result.textContent = data.english;
        };
    }
};
