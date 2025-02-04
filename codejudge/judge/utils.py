import subprocess
import re

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
        # Extract the class name using regex
        match = re.search(r'public\s+class\s+(\w+)', code)
        
        if not match:
            return "Compilation Error: No public class found in the Java code."

        class_name = match.group(1)  # Extracted class name
        filename = f"{class_name}.java"

        # Write the Java code to the correct file
        with open(filename, "w") as file:
            file.write(code)
        
        # Compile Java Code
        compile_command = ["javac", filename]
        try:
            subprocess.run(compile_command, check=True, capture_output=True, text=True)

            # Run the Java program using the Java runtime
            # Pass the dynamic input_data to the Java program
            run_command = ["java", class_name]
            result = subprocess.run(run_command, input=input_data + "\n", capture_output=True, text=True)

            return result.stdout.strip() if result.stdout else "Execution Error"
        except subprocess.CalledProcessError as e:
            return f"Compilation Error: {e.stderr.strip() if e.stderr else 'Unknown error'}"
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
