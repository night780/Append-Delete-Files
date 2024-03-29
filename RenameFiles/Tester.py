import os
import random
import string


def generate_random_filename():
    """Generates a random filename consisting of 6 letters and digits."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


def main():
    print("Welcome to the File Creator Tool")
    dir_path = input("Enter the directory path where you want to add files: ")

    while not os.path.isdir(dir_path):
        print("Invalid directory path. Please try again.")
        dir_path = input("Enter the directory path where you want to add files: ")

    try:
        num_files = int(input("How many files do you want to create? "))
    except ValueError:
        print("Invalid number. Exiting.")
        return

    for _ in range(num_files):
        filename = generate_random_filename() + ".txt"  # Assuming text files for simplicity
        file_path = os.path.join(dir_path, filename)

        # Create the file and optionally write data to it
        with open(file_path, 'w') as file:
            file.write("This is a randomly named file.\n")  # Example content

        print(f"Created file: {file_path}")

    print(f"{num_files} files successfully created in {dir_path}")


if __name__ == "__main__":
    main()
