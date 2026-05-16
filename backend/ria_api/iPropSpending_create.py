def iPropSpending_create():
    # Create a proportional spending income data structure
    return {
        'investedAmount': 100000,
        'useRMDlifeExpectancies': 'y',
        'nonRMDlifeExpectancies': [],
        'nonRMDfirstLEAge': 70,
        'portfolioOwnerCurrentAge': 65,
        'showProportionsSpent': 'n',
        'showLockboxEquivalentValues': 'n',
        'glidePath': np.array([[1.0], [1]]),
        'showGlidePath': 'n',
        'retentionRatio': 0.999
    }
