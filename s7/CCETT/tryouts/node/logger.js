const microphone = require('node-microphone');
const iohook = require('iohook');

let mic;
let isMicrophoneStarted = false;
let isKeyboardStarted = false;

function startMicrophone() {
  if (!isMicrophoneStarted) {
    mic = microphone({
      rate: 44100,
      channels: 1,
      debug: true,
    });

    mic.on('data', (data) => {
      const volumeLevel = Math.max(...data);
      console.log('Noise level:', volumeLevel);
    });

    mic.on('error', (error) => {
      console.error(error);
    });

    mic.startRecording();
    isMicrophoneStarted = true;
  } else {
    console.log('Microphone is already started.');
  }
}

function stopMicrophone() {
  if (isMicrophoneStarted) {
    mic.stopRecording();
    isMicrophoneStarted = false;
    console.log('Microphone stopped.');
  } else {
    console.log('Microphone is not started.');
  }
}

function startKeyboard() {
  if (!isKeyboardStarted) {
    iohook.on('keydown', (event) => {
      console.log('Key pressed:', event.keycode);
    });

    iohook.start();
    isKeyboardStarted = true;
    console.log('Keyboard input detection started.');
  } else {
    console.log('Keyboard input detection is already started.');
  }
}

function stopKeyboard() {
  if (isKeyboardStarted) {
    iohook.removeListener('keydown');
    iohook.stop();
    isKeyboardStarted = false;
    console.log('Keyboard input detection stopped.');
  } else {
    console.log('Keyboard input detection is not started.');
  }
}

// Usage examples
startMicrophone();
startKeyboard();

// Stop microphone and keyboard input detection after 10 seconds
setTimeout(() => {
  stopMicrophone();
  stopKeyboard();
}, 10000); // Stop after 10 seconds (10000 milliseconds)
