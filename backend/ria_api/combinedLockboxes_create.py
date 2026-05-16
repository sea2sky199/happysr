def combinedLockboxes_create():
    # creates a lockbox by combining other lockboxes
    combinedLockboxes = {}
    combinedLockboxes['componentLockboxes'] = []
	# proportions of lockboxes being combined
    # one value for each lockbox; values greater than or equal to 0
    # values will be normalized to sum to 1.0
    combinedLockboxes['componentWeights'] = []
    combinedLockboxes['title'] = 'Combined Lockboxes'
    combinedLockboxes['proportions'] = []
    combinedLockboxes['showCombinedProportions'] = 'n'
    return combinedLockboxes