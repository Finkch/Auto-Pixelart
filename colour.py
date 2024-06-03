# Tracks colour and colour operations
from numpy import average

# Returns the average colour in a set of colours
def average_colour(colours):

    # In the case `colours` contains frequency information
    if isinstance(colours[1], tuple):
        return (
            int(average([colour[0] for colour in colours])),
            (
                int(average([colour[1][0] for colour in colours])), 
                int(average([colour[1][1] for colour in colours])), 
                int(average([colour[1][2] for colour in colours])),
            )
        )
    
    # When `colours` is only RGB
    else:
        return (
                int(average([colour[0] for colour in colours])), 
                int(average([colour[1] for colour in colours])), 
                int(average([colour[2] for colour in colours])),
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


# An easy way of getting the list of functions in this file
colour_functions    = [average_colour, weighted_colour, common_colour]
colour_names        = ['Average', 'Weighted', 'Common']