
def add(a, b):
    return a + b
  # User's function

def run_tests():
    test_cases = [{'input': [2, 3], 'expected': 5}, {'input': [5, 7], 'expected': 12}, {'input': [-1, 1], 'expected': 0}]
    results = []
    for test in test_cases:
        args, expected = test["input"], test["expected"]
        try:
            output = add(*args)
            results.append({"input": args, "expected": expected, "output": output, "pass": output == expected})
        except Exception as e:
            results.append({"input": args, "expected": expected, "output": str(e), "pass": False})
    print(json.dumps(results))

run_tests()
