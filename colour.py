# Tracks colour and colour operations
from numpy import average

# Returns the average colour in a set of colours
def average_colour(colours):
    return (
        int(average([colour[0] for colour in colours])),
        (
            int(average([colour[1][0] for colour in colours])), 
            int(average([colour[1][1] for colour in colours])), 
            int(average([colour[1][2] for colour in colours])),
        )
    )

# Same as average_colour(), but where the weights are the occurances
def weighted_colour(colours):
    weights = [colour[0] for colour in colours]
    return (
        int(average([colour[0] for colour in colours])),
        (
            int(average([colour[1][0] for colour in colours], weights = weights)), 
            int(average([colour[1][1] for colour in colours], weights = weights)), 
            int(average([colour[1][2] for colour in colours], weights = weights)),
        )
    )

# Returns the most common colour in a set
def common_colour(colours):
    return max(colours, key = lambda x : x[0])

