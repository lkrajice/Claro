import os


def get_version():
    """
    Parse version of program

    Returns:
        (tuple): contains:
            version number (e.g. v1.3 or v0.1)
            release (e.g. alpha-v1.3, pre-v0.1)
    """
    directory = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(directory, '..', 'VERSION'), 'r') as f:
        release_type, release_number = f.readline().strip().split(' ')
        return release_number, '{}-{}'.format(release_type, release_number)
