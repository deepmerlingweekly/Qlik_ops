const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let pyProc = null;
let mainWindow = null;

function startPython() {
  const script = path.join(__dirname, 'backend', 'app.py');
  const isDev = !app.isPackaged;

  let pythonPath;

  if (process.platform === 'win32') {
    if (isDev) {
      // in dev: punta alla cartella locale python_qlik
      pythonPath = path.join(__dirname, 'python_qlik', 'Scripts', 'python.exe');
    } else {
      // in build: punta a resources/python_qlik
      pythonPath = path.join(process.resourcesPath, 'python_qlik', 'Scripts', 'python.exe');
    }
  } else {
    // macOS / Linux
    if (isDev) {
      pythonPath = path.join(__dirname, 'python_qlik', 'bin', 'python3');
    } else {
      pythonPath = path.join(process.resourcesPath, 'python_qlik', 'bin', 'python3');
    }
  }

  pyProc = spawn(pythonPath, [
    "-m", "streamlit", "run", script,
    "--server.port=8501",
    "--server.headless=true"
  ]);

  pyProc.stdout.on('data', (data) => {
    console.log(`PYTHON: ${data}`);
  });

  pyProc.stderr.on('data', (data) => {
    console.error(`PYTHON ERROR: ${data}`);
  });

  pyProc.on('close', (code) => {
    console.log(`Streamlit exited with code ${code}`);
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: { nodeIntegration: false }
  });

  mainWindow.loadURL('http://localhost:8501');
}

app.on('ready', () => {
  startPython();
  setTimeout(createWindow, 4000);
});

app.on('will-quit', () => {
  if (pyProc) pyProc.kill();
});
