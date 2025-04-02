
def print_attributes_M(pattern):
    # See attributes
    for cmd in pattern.commands:
        if cmd.__dict__.get("name") == "M":
            print(cmd.__dict__)

def print_attributes_N(pattern):
    # See attributes
    for cmd in pattern.commands:
        if cmd.__dict__.get("name") == "N":
            print(cmd.__dict__)

def print_attributes_E(pattern):
    # See attributes
    for cmd in pattern.commands:
        if cmd.__dict__.get("name") == "E":
            print(cmd.__dict__)

def print_attributes_C(pattern):
    # See attributes
    for cmd in pattern.commands:
        if cmd.__dict__.get("name") == "C":
            print(cmd.__dict__)