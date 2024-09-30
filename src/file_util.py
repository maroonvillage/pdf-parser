import os


def check_for_file(file_path):

    if os.path.isfile(file_path):
        return True
    else:
        return False


def read_lines_into_list(file_path):

    my_dict = {}
    keys = []
    values = []
    line_no = 1
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read and print each line one by one
        for line in file:
            #keys.append(line_no)
            stripped_line = line.strip()
            values.append(stripped_line)
            #print(line.strip())  # Use strip() to remove any leading/trailing whitespace
        print('Finished reading the file.')

    return values




