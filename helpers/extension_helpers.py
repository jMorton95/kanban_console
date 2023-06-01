def convert_float_to_time(time_float):
    hours = int(time_float)
    minutes = (time_float - hours) * 60
    return hours, round(minutes)


def validate_as_int(input: str):
    try:
        int(input)
        return True
    except ValueError:
        return False
    
def validate_as_float(input: str):
    try:
        float(input)
        return True
    except ValueError:
        return False
    
def find_option_by_number(options: list[str], user_input: int):
    #Search our pre-defined List of outputs with with a user input. Format example: "3: User Option..."
    return next((opt for opt in options if (int(opt[0]) == user_input)), "Unknown Option")

def check_option_in_range(options: int | float, opt: int | float):
    return True if opt <= options else False