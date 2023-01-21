innovation_number = 0

def get_new_innovation_number() -> int:
    global innovation_number
    innovation_number += 1
    return innovation_number
        