# A quick little logging tool

# Logs data it is passed
def log(data, file):
    
    # Location of the logs directory
    loc = 'logs'

    # Writes the data to the file
    # The data is overwritten
    with open(f'{loc}/{file}.txt', 'w') as f:
        for line in data:
            f.write(line)