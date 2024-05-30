# Tracks colour and colour operations

# Returns the average colour in a set of colours
def average_colour(colours):
    return (
        int(sum(colour[0] for colour in colours) / len(colours)),
        (
            int(sum([colour[1][0] for colour in colours]) / len(colours)), 
            int(sum([colour[1][1] for colour in colours]) / len(colours)), 
            int(sum([colour[1][2] for colour in colours]) / len(colours)),
        )
    )

# Returns the most common colour in a set
def common_colour(colours):
    return max(colours, key = lambda x : x[0])

