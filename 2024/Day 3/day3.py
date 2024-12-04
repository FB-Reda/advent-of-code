import re

def process_memory(filename):
    # Read the input file
    with open(filename, 'r') as file:
        data = file.read()
    
    # Regular expression to find valid mul(X,Y) instructions
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, data)
    
    # Calculate the sum of the products
    total_sum = 0
    for x, y in matches:
        product = int(x) * int(y)
        total_sum += product
        #print(f"Valid instruction: mul({x},{y}) -> {product}")
    
    return total_sum

def process_memory_with_conditions(filename):
    # Read the input file
    with open(filename, 'r') as file:
        data = file.read()
    
    # Regular expressions for different instructions
    mul_pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    do_pattern = r"do\(\)"
    dont_pattern = r"don't\(\)"

    # Initialize state
    enabled = True
    total_sum = 0

    # Scan through the input
    position = 0
    while position < len(data):
        # Check for the next instruction
        mul_match = re.search(mul_pattern, data[position:])
        do_match = re.search(do_pattern, data[position:])
        dont_match = re.search(dont_pattern, data[position:])

        # Find the earliest match
        next_instruction = None
        next_position = len(data)
        if mul_match:
            next_instruction = "mul"
            next_position = position + mul_match.start()
        if do_match and position + do_match.start() < next_position:
            next_instruction = "do"
            next_position = position + do_match.start()
        if dont_match and position + dont_match.start() < next_position:
            next_instruction = "don't"
            next_position = position + dont_match.start()

        # If no instruction is found, break
        if next_instruction is None:
            break

        # Process the instruction
        if next_instruction == "mul":
            x, y = map(int, mul_match.groups())
            if enabled:
                product = x * y
                total_sum += product
                # print(f"Enabled mul({x},{y}) -> {product}")
            #else:
                #print(f"Disabled mul({x},{y})")
            position += mul_match.end()  # Move past this instruction
        elif next_instruction == "do":
            enabled = True
            #print("do() -> Enabling future mul instructions")
            position += do_match.end()  # Move past this instruction
        elif next_instruction == "don't":
            enabled = False
            #print("don't() -> Disabling future mul instructions")
            position += dont_match.end()  # Move past this instruction

    return total_sum

if __name__ == "__main__":
    # Input file name
    input_file = "input.txt"
    
    # Process the input and calculate the total sum
    result = process_memory(input_file)
    print(f"\nTotal sum of valid mul(X,Y) instructions: {result}")

    # Process the input and calculate the total sum with conditions
    result = process_memory_with_conditions(input_file)
    print(f"\nTotal sum of valid mul(X,Y) instructions: {result}")
