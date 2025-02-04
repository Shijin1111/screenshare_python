# core/utils.py
import subprocess
import tempfile
import os

def evaluate_code(code, language, problem_id):
    problem = Problem.objects.get(id=problem_id)
    result = "failed"

    # Handle Python code
    if language == "python":
        try:
            # Check if the code matches the expected function signature
            if problem.expected_python_signature not in code:
                return "failed"
            exec(code)  # WARNING: Unsafe for production, use Docker instead
            nums = [2, 7, 11, 15]
            target = 9
            expected_output = [0, 1]
            output = twoSum(nums, target)  # Assume 'twoSum' is the function defined by the user
            if output == expected_output:
                result = "passed"
        except Exception as e:
            result = "failed"

    # Handle C++ code
    elif language == "cpp":
        try:
            # Save C++ code to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp") as code_file:
                code_file.write(code.encode())
                code_file.close()

                # Compile the C++ code
                compile_command = f"g++ {code_file.name} -o {code_file.name}.out"
                compile_result = subprocess.run(compile_command, shell=True, capture_output=True)
                
                if compile_result.returncode != 0:
                    result = "failed"
                    os.remove(code_file.name)
                    return result

                # Execute the compiled C++ code
                execute_command = f"./{code_file.name}.out"
                execution_result = subprocess.run(execute_command, shell=True, capture_output=True, text=True)
                
                if execution_result.returncode == 0:
                    output = execution_result.stdout.strip().split("\n")
                    expected_output = ["0", "1"]
                    if output == expected_output:
                        result = "passed"
                os.remove(code_file.name)
        except Exception as e:
            result = "failed"

    # Handle Java code
    elif language == "java":
        try:
            # Save Java code to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".java") as code_file:
                code_file.write(code.encode())
                code_file.close()

                # Compile the Java code
                compile_command = f"javac {code_file.name}"
                compile_result = subprocess.run(compile_command, shell=True, capture_output=True)

                if compile_result.returncode != 0:
                    result = "failed"
                    os.remove(code_file.name)
                    return result

                # Run the Java code
                class_name = os.path.basename(code_file.name).replace(".java", "")
                execute_command = f"java {class_name}"
                execution_result = subprocess.run(execute_command, shell=True, capture_output=True, text=True)

                if execution_result.returncode == 0:
                    output = execution_result.stdout.strip().split("\n")
                    expected_output = ["0", "1"]
                    if output == expected_output:
                        result = "passed"
                os.remove(code_file.name)
        except Exception as e:
            result = "failed"

    return result
