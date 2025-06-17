const input = document.getElementById('freq-input');
const display = document.getElementById('freq-display');
const circle=document.getElementById("rotatingCircle")

let frequency=0;
let angle=0;

function rotateCircle(){
  const rpm=frequency*60;
  const degPerSec = (rpm / 60) * 360;
  angle = (angle + degPerSec / 60) % 360; // 60 FPS
  circle.style.transform = `rotate(${angle}deg)`;
    requestAnimationFrame(rotateCircle);
}

freqInput.addEventListener("input", (e) => {
    frequency = parseFloat(e.target.value) || 0;
    document.getElementById("freq-display").textContent = `Current Frequency: ${frequency.toFixed(2)} Hz`;
});

rotateCircle();

input.addEventListener('input', () => {
  const value = input.value;
  display.textContent = `Frequency Entered: ${value} Hz`;
  fetch('http://localhost:3000/setfrequency',{
    method:'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ frequency: value })
  })
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);
  })
  .catch(error => {
    console.error('Error:', error);
  });
});
