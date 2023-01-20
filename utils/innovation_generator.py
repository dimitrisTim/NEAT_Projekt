from connection import Connection

innovation_number = 0
innovations: list[Connection] = []

def get_new_innovation_number() -> int:
    global innovation_number
    innovation_number += 1
    return innovation_number

def create_connection(input_id, output_id):
    for innovation in innovations:
        if innovation.input == input_id and innovation.output == output_id:            
            return innovation
    new_innovation = Connection(input_id, output_id)
    innovations.append(new_innovation)
    return new_innovation
        