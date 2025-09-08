const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const os = require('os');
const fs = require('fs');
const http = require('http');

let pyProc = null;
let mainWindow = null;

// Log su file
const logFile = path.join(app.getPath('userData'), 'electron.log');
function log(msg) {
  fs.appendFileSync(logFile, `[${new Date().toISOString()}] ${msg}\n`);
}

// Attende che Streamlit sia pronto su localhost:8501
function waitForServer(url, timeout = 30000) {
  return new Promise((resolve, reject) => {
    const start = Date.now();
    const check = () => {
      http.get(url, () => resolve()).on('error', () => {
        if (Date.now() - start > timeout) reject(new Error('Streamlit timeout'));
        else setTimeout(check, 500);
      });
    };
    check();
  });
}

// Avvia Python + Streamlit
function startPython() {
  const isDev = !app.isPackaged;
  const resourcesPath = isDev ? __dirname : process.resourcesPath;
  log(__dirname)
  log(process.resourcesPath)
  let pythonExe;

  if (process.platform === 'win32') {
    pythonExe = path.join(resourcesPath, 'python_embedded', 'python.exe');
  } else {
    pythonExe = path.join(resourcesPath, 'python_embedded', 'bin', 'python3');
  }
  const streamlitScript = path.join(resourcesPath, 'backend', 'app.py');
  log(`chosen python: ${pythonExe}`);
  pyProc = spawn(pythonExe, [
    '-m', 'streamlit', 'run', streamlitScript,
    '--server.port', '8501',
    '--server.headless', 'true'
  ]);

  pyProc.stdout.on('data', (data) => log(`STDOUT: ${data}`));
  pyProc.stderr.on('data', (data) => log(`STDERR: ${data}`));
  pyProc.on('close', (code) => log(`Streamlit exited with code ${code}`));

  log('Avviato Streamlit');
}

// Crea finestra Electron
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: { devTools: false } // abilita devtools
  });

  mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription) => {
    log(`WebContents failed to load: ${errorCode} - ${errorDescription}`);
  });

  mainWindow.loadURL('http://localhost:8501');
}

app.on('ready', async () => {
  startPython();
  log('Attendo che Streamlit sia pronto su http://localhost:8501 ...');
  try {
    await waitForServer('http://localhost:8501');
    log('Streamlit pronto, creo finestra Electron');
    createWindow();
  } catch (err) {
    log(`Errore: ${err.message}`);
    createWindow();
    mainWindow.loadURL('data:text/html,<h1>Errore avviando Streamlit</h1>');
  }
});

app.on('will-quit', () => {
  if (pyProc) {
    log('Chiudo processo Streamlit');
    pyProc.kill();
  }
});
