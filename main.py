from PlanManager import PlanManager

import sys

def parse_arguments():
    """Parse les arguments passés au script et retourne un dictionnaire."""
    args = sys.argv[1:]  # Ignore le nom du script lui-même
    arguments = {}

    for arg in args:
        if '=' in arg:
            key, value = arg.split('=')
            arguments[key] = value
        else:
            arguments[arg] = True  # Pour les flags
    
    return arguments

if __name__ == "__main__":
    arguments = parse_arguments()
    if "env" in arguments:
        PlanManager.get_instance(arguments["env"]).go()
    else:
        PlanManager.get_instance().go() # If you want to randomly generate the environment 
