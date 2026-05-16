def iSocialSecurity_create():
    # Incomes in state 1, last column repeated for subsequent years
    state1Incomes = [np.inf, 30000]

    # Incomes in state 2, last column repeated for subsequent years
    state2Incomes = [np.inf, 30000]

    # Incomes for state 3, last column repeated for subsequent years
    state3Incomes = [44000]

    return {
        'state1Incomes': state1Incomes,
        'state2Incomes': state2Incomes,
        'state3Incomes': state3Incomes
    }
