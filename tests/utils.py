import os


def get_resources_path(test_file_name: str) -> str:
    """Constructs the path to the resources folder of the test case based on the current file name.

    Args:
        test_file_name (str): The name of the test file

    Returns:
        str: The full path to the resources folder
    """
    basename = os.path.basename(test_file_name)
    filename = os.path.splitext(basename)[0]
    foldername = filename.removeprefix("test_")
    basepath = os.path.dirname(test_file_name)
    return os.path.join(basepath, foldername)


def read_file(filepath: str) -> str:
    """Return the contents of a raw text file.

    Args:
        filepath (str): The path to the raw text file

    Returns:
        str: The raw text file contents
    """
    with open(filepath, "r") as file:
        content = file.read()
    return content
