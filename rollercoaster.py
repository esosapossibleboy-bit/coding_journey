def check_rider(height_cm):
    # Rule 1: If height_cm is less than 100, return "Too short to ride!"
    if height_cm < 100:
        return "Too short to ride!"
    # Rule 2: If height_cm is 100 or more, return "Have a fun ride!"
    else:
        return "Have a fun ride!"
