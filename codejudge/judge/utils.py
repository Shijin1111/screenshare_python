import subprocess

def execute_code(code, language, input_data):
    if language == "python":
        command = ["python3", "-c", code]
    elif language == "cpp":
        with open("temp.cpp", "w") as file:
            file.write(code)
        command = ["g++", "-o", "temp", "temp.cpp"]
        try:
            subprocess.run(command, check=True)
            command = ["./temp"]
        except subprocess.CalledProcessError as e:
            return f"Compilation Error: {e.stderr.decode()}"
    elif language == "java":
        with open("Main.java", "w") as file:
            file.write(code)
        command = ["javac", "Main.java"]
        try:
            subprocess.run(command, check=True)
            command = ["java", "Main"]
        except subprocess.CalledProcessError as e:
            return f"Compilation Error: {e.stderr.decode()}"
    else:
        return "Error: Unsupported language"

    try:
        process = subprocess.run(command, input=input_data, text=True, capture_output=True, timeout=5)
        if process.returncode != 0:
            return f"Runtime Error: {process.stderr.strip()}"
        return process.stdout.strip()  # Return the output of execution
    except subprocess.TimeoutExpired:
        return "Time Limit Exceeded"
    except Exception as e:
        return f"Error: {str(e)}"
