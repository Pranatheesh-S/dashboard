const input = document.getElementById('freq-input');
const display = document.getElementById('freq-display');

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
