# Tracks colour and colour operations
from numpy import average

# Returns the average colour in a set of colours
def average_colour(colours):

    # In the case `colours` contains frequency information
    if isinstance(colours[0][1], tuple):
        return (
            int(average([colour[0] for colour in colours])),
            get_average_colour(colours)
        )
    
    # When `colours` is only RGB
    else:
        return get_average_colour(colours)

# Same as average_colour(), but where the weights are the occurances
def weighted_colour(colours):
    weights = [colour[0] for colour in colours]
    return (
        int(average(weights)),
        get_average_colour(colours, weights)
    )

# Returns the most common colour in a set
def common_colour(colours):
    return max(colours, key = lambda x : x[0])

# Gets the average colour
def get_average_colour(colours, weights = None):

    # One recursive call to remove frequency component
    if isinstance(colours[0][1], tuple):
        return get_average_colour([colour[1] for colour in colours], weights)

    # Averages each channel
    return (
        int(average([colour[0] for colour in colours], weights = weights)),
        int(average([colour[1] for colour in colours], weights = weights)),
        int(average([colour[2] for colour in colours], weights = weights))
    )


# An easy way of getting the list of functions in this file
colour_functions    = [average_colour, weighted_colour, common_colour]
colour_names        = ['Average', 'Weighted', 'Common']