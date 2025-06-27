from entropy import *

def score(password):
    entropy = calculate_entropy(password)
    if entropy<= 35:
        return "Très faible", 25, "red"
    elif entropy>=36 and entropy<=59:
        return "Faible", 50, "orange"
    elif entropy>=60 and entropy<=119:
        return "Fort", 75, "yellow"
    elif entropy>=120:
        return "Très Fort", 100, "green"