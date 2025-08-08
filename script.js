const video = document.getElementById('video');
const loaderBar = document.getElementById('loader-bar');
const statusText = document.getElementById('status');

let progress = 0;
let looking = false;
let funnyMessages = [
  "Looking for your beautiful face... 😏",
  "Don't blink! 👀",
  "Where did you go? 🤨",
  "Stay with me... 😌",
  "Almost there! 🚀"
];

// Start webcam
async function startVideo() {
  const stream = await navigator.mediaDevices.getUserMedia({ video: {} });
  video.srcObject = stream;
}

// Load models
Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri('https://justadudewhohacks.github.io/face-api.js/models'),
]).then(startVideo);

// Detect faces
video.addEventListener('play', () => {
  let msgIndex = 0;
  const detectInterval = setInterval(async () => {
    const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions());
    looking = detections.length > 0;

    if (looking) {
      progress = Math.min(progress + 1, 100);
      statusText.textContent = funnyMessages[msgIndex % funnyMessages.length];
      msgIndex++;
    } else {
      progress = Math.max(progress - 2, 0);
      statusText.textContent = "Paused! I miss your face 😢";
    }

    loaderBar.style.width = progress + '%';

    if (progress >= 100) {
      statusText.textContent = "✅ Loaded! You're amazing! 🎉";
      loaderBar.style.background = "gold";
      clearInterval(detectInterval);
    }
  }, 200);
});
