# Read input as a comma-separated list
height = list(map(int, input().split(',')))

# Two-pointer approach to find max area
left, right = 0, len(height) - 1
max_area = 0

while left < right:
    width = right - left
    max_area = max(max_area, min(height[left], height[right]) * width)
    
    if height[left] < height[right]:
        left += 1
    else:
        right -= 1

print(max_area)
