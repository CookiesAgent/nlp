import random

def select_random_chunks(file_path, num_chunks):
    chunks = []
    with open(file_path, 'r', encoding="utf8") as file:
        lines = file.readlines()
        total_lines = len(lines)
        for _ in range(num_chunks):
            chunk_size = random.randint(1, 3)  # Choose a random chunk size between 1 and 3
            start_index = random.randint(0, total_lines - chunk_size)
            chunk = ''.join(lines[start_index:start_index + chunk_size])
            chunks.append(chunk)
    return chunks

def write_chunks_to_file(chunks, output_file):
    with open(output_file, 'w', encoding="utf8") as file:
        for chunk in chunks:
            file.write(chunk.strip() + '\n')  # Write the chunk with a newline
            file.write("~\n")  # Separate chunks with a line "~"

file_path = 'gutenberg_edited.txt'  # Replace 'your_file.txt' with the path to your file
output_file = 'gutenberg_test.txt'  # Specify the output file path
num_chunks = 10000
random_chunks = select_random_chunks(file_path, num_chunks)

write_chunks_to_file(random_chunks, output_file)
