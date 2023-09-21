const { spawn } = require("child_process");

// Define the relative path to the Python executable
const pythonExecutable = "/usr/bin/python3"; // Or './path/to/python' if it's not in PATH

// Define the path to the Python script
const pythonScript = "../app.py";

function runPythonScript() {
  const pythonProcess = spawn(pythonExecutable, [pythonScript]);

  pythonProcess.stdout.on("data", (data) => {
    console.log(`Python Output: ${data}`);
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`Python Error: ${data}`);
  });

  pythonProcess.on("close", (code) => {
    console.log(`Python process exited with code ${code}`);

    // Re-run the Python script after a delay (e.g., 100ms)
    console.log("Restarting Python script...");
    setTimeout(runPythonScript, 100); // 100ms (adjust as needed)
  });
}

// Initial run of the Python script
runPythonScript();
