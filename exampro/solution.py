# Read user input
input_str = input()

# Split the input by semicolon
nums_str, target_str = input_str.split(';')

# Convert nums to list of integers and target to an integer
nums = list(map(int, nums_str.split(',')))
target = int(target_str)

# Two Sum logic
num_map = {}
for i, num in enumerate(nums):
    complement = target - num
    if complement in num_map:
        print([num_map[complement], i])
        break
    num_map[num] = i
