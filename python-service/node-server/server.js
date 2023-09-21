const express = require("express");
const { spawn } = require("child_process");
const http = require("http");
const socketIo = require("socket.io");
const fs = require("fs");

// Define the relative path to the Python executable
const pythonExecutable = "/usr/bin/python3"; // Or './path/to/python' if it's not in PATH

// Define the path to the Python script
const pythonScript = "../app.py";

function runPythonScript(socket) {
  const pythonProcess = spawn(pythonExecutable, [pythonScript]);

  console.log("Python process started");
  socket.emit("python-started"); // Send a message to the client that the Python script has started
  
  pythonProcess.stdout.on("data", (data) => {
    console.log(`Python Output: ${data}`);
    socket.emit("python-output", data.toString()); // Send Python output to the client
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`Python Error: ${data}`);
    socket.emit("python-error", data.toString()); // Send Python error to the client
  });

  pythonProcess.on("close", (code) => {
    console.log(`Python process exited with code ${code}`);
    socket.emit("python-exit", code); // Send Python exit code to the client
    runPythonScript(socket); // Restart the Python script
  });
}

// Create an Express application
const app = express();
const server = http.createServer(app);
const io = socketIo(server);
const port = 3000; // Set your desired port number

// Serve static files (e.g., HTML, GIFs)
app.use(express.static(__dirname));

// Define a route to serve the initial HTML page
app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

// WebSocket connection handling
io.on("connection", (socket) => {
  // Send initial status to the client
  runPythonScript(socket);

  // Handle client disconnect
  socket.on("disconnect", () => {
    // Stop the Python script (if running) when the client disconnects
    // You can add logic to handle this case if needed
  });
});

// Start the Express server
server.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
