const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const dialog = electron.dialog;
const production = true;
electron.crashReporter.start({
  productName: 'GeometrA',
  companyName: 'NTUT',
  submitURL: 'https://localhost:5000',
  uploadToServer: true
});

var mainWindow = null;

app.on('window-all-closed', function() {
  // if (process.platform != 'darwin') {
  app.quit();
  //}
});
app.commandLine.appendSwitch("--disable-http-cache")
app.on('ready', function() {
  // call python?
  if (process.platform === 'win32')
    var subpy = require('child_process').spawn('py', ['./main.py']);
  else
    var subpy = require('child_process').spawn('python3', ['./main.py']);
  var rq = require('request-promise');
  var mainAddr = 'http://localhost:5000';

  var openWindow = function() {
    mainWindow = new BrowserWindow(
        {width: 1920, height: 1080, webPreferences: {webSecurity: false}});
    // mainWindow.loadURL('file://' + __dirname + '/index.html');
    mainWindow.loadURL('http://localhost:5000');
    if (!production) mainWindow.webContents.openDevTools();
    mainWindow.on('closed', function() {
      mainWindow = null;
      subpy.kill('SIGINT');
    });
  };

  app.on('activate', function() {
    if (mainWindow === null) {
      openWindow()
    }
  })

  var startUp = function() {
    rq(mainAddr)
        .then(function(htmlString) {
          console.log('server started!');
          openWindow();
        })
        .catch(function(err) {
          // console.log('waiting for the server start...');
          startUp();
        });
  };

  // fire!
  startUp();
});

exports.selectDirectory =
    function(callback) {
  dialog.showOpenDialog(
      mainWindow, {properties: ['openDirectory'], multiSelections: false},
      callback);
}

exports.selectProject = function(callback) {
  const dialogOption = {
    filters: [
      {name: 'Test Project', extensions: ['json']},
    ],
    properties: ['openFile'],
    multiSelections: false
  };
  dialog.showOpenDialog(mainWindow, dialogOption, callback);
}