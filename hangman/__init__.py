class colors:
    RED = '\033[31m'
    END = '\033[0m'
    BLUE = '\033[96m'


# The Configurations contains all the configurations that can be done through the
# command line arguments.
class Configurations:
    def __init(self, lives=10, min_length=2, max_length=10):
        pass



# The state of the system describes the to be guessed word, 
# all the wrongly guessed characters, the current progress of the word, 
# the number of Lives and the configuration options.
class State:
    def __init__(self, configurations):
        self.lives = configurations.lives

        

def print_error(string):
    print(f"{colors.RED}{string}{colors.END}")

def print_info(string):
    print(f"{colors.BLUE}{string}{colors.END}")

