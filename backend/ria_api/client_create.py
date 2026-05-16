def client_create():
    # create a client data structure with default values
    client = {
        'p1Name': 'Bob',
        'p1Sex': 'M',
        'p1Age': 67,
        'p2Name': 'Sue',
        'p2Sex': 'F',
        'p2Age': 65,
        'Year': 2015,
        'nScenarios': 100000,
        'budget': 1000000,
        # figure size in pixels: width, height
        # set to [] to use full screen
        'figureSize': [1500, 900]
    }
    return client