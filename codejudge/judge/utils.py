import subprocess

def execute_code(code, language, input_data):
    if language == "python":
        command = ["python3", "-c", code]
    elif language == "cpp":
        command = ["g++", "-o", "temp", "temp.cpp", "&&", "./temp"]
    elif language == "java":
        command = ["java", "Main.java"]
    else:
        return "Error: Unsupported language"

    try:
        process = subprocess.run(command, input=input_data, text=True, capture_output=True, timeout=5)
        return process.stdout.strip()  # Return the output of execution
    except subprocess.TimeoutExpired:
        return "Time Limit Exceeded"
    except Exception as e:
        return f"Error: {str(e)}"
