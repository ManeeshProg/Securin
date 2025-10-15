print("hi")

# Method 1: Using slicing (most Pythonic)
def reverse_string_slice(s):
    return s[::-1]

# Method 2: Using reversed() and join()
def reverse_string_reversed(s):
    return ''.join(reversed(s))

# Method 3: Using a loop
def reverse_string_loop(s):
    reversed_str = ""
    for char in s:
        reversed_str = char + reversed_str
    return reversed_str

# Test the functions
if __name__ == "__main__":
    test_string = "Hello, World!"

    print(f"Original: {test_string}")
    print(f"Method 1 (slicing): {reverse_string_slice(test_string)}")
    print(f"Method 2 (reversed): {reverse_string_reversed(test_string)}")
    print(f"Method 3 (loop): {reverse_string_loop(test_string)}")