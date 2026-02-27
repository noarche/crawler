import os

def split_domains(file_path, part, delimiter):
    # Read the content of the file
    with open(file_path, 'r') as file:
        domains = file.readlines()

    # Prepare the list of stripped domains
    stripped_domains = []
    for domain in domains:
        # Remove leading/trailing whitespace
        domain = domain.strip()
        # Split the domain by the first occurrence of the user-provided delimiter
        parts = domain.split(delimiter, 1)
        if len(parts) == 2:
            # Choose the part based on user input (first or second half)
            stripped_domains.append(parts[part])

    # Create the new file name
    dir_name, base_name = os.path.split(file_path)
    new_file_name = os.path.join(dir_name, base_name.replace('list.txt', 'list-stripped.txt'))

    # Write the stripped domains to the new file
    with open(new_file_name, 'w') as new_file:
        for domain in stripped_domains:
            new_file.write(domain + '\n')

    print(f"Stripped domains have been saved to: {new_file_name}")

def main():
    # Prompt the user for which half to keep (1 for first half, 2 for second half)
    choice = input("Enter 1 to keep the first half of the domain or 2 to keep the second half: ")
    
    if choice == '1':
        part = 0
    elif choice == '2':
        part = 1
    else:
        print("Invalid choice. Please run the script again and enter 1 or 2.")
        return

    # Prompt the user for the delimiter
    delimiter = input("Please enter the delimiter to split the domains: ")

    # Specify the source file
    source_file = "list.txt"
    if os.path.isfile(source_file):
        split_domains(source_file, part, delimiter)
    else:
        print("The file 'list.txt' does not exist. Please ensure it is in the correct directory.")

if __name__ == "__main__":
    main()
