def replace_text_in_file(file_path: str, variable_to_replace: str, new_value: str):
    """
    Reads the content of a file, replaces all occurrences of a specified variable
    with a new value, and returns the modified content.

    :param file_path: Path of the file to be modified.
    :param variable_to_replace: The variable whose value should be replaced in the text.
    :param new_value: The new value to replace the variable with.
    :return: The content of the file with the variable replaced by the new value.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        modified_content = content.replace(variable_to_replace, new_value)

        return modified_content
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return None
    except IOError:
        print(f"Error accessing the file {file_path}.")
        return None

if __name__ == "__main__":
    # Example usage when the script is run directly
    file_path = '../prompts/controls_prompt_en.txt'  # Path to the input file
    variable_to_replace = 'PRODUCT_NAME'  # The variable to be replaced
    new_value = 'SuperSecure'  # The new value for the variable

    # Call the function with the example parameters
    modified_content = replace_text_in_file(file_path, variable_to_replace, new_value)

    if modified_content is not None:
        print(modified_content)
