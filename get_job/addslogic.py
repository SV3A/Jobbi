from random import seed, randint


def shuffle_adds(seq_adds):
    """ Mixes sequential data loaded from DB """

    # Container for each provider and associated adds (JobAdd object in list)
    data_dict = {}

    # List containing tuples each containing job providers and number of adds
    size_idx = []

    # Ouput adds
    mixed_adds = []

    # First divide the input list into its unique identifiers (add_owner) i.e.
    # add provider e.g. "jobfinder"
    for add in seq_adds:
        provider = add.add_owner

        if provider not in data_dict:
            data_dict[provider] = []

        data_dict[provider].append(add)

    # Make index over size (number of adds) for each provider
    for provider in data_dict:
        size_idx.append((provider, len(data_dict[provider])))

    # List
    provider_idx = [x for x in range(1, len(size_idx)+1)]

    # List containing the increment index for each provider
    current_idx = [0 for x in range(1, len(size_idx)+1)]

    # Mix adds from all providers
    seed(1)
    done = False
    while not done:
        for i in range(len(provider_idx)):
            adds = data_dict[size_idx[i][0]]

            # If only one source left append all adds and terminate
            if len(provider_idx) == 1:
                mixed_adds = mixed_adds + adds[current_idx[i]:]
                done = True
                break

            # Increment index by 2 or 3
            end_idx = current_idx[i] + randint(2, 3)

            # If increment overshoot list limit remove provider from
            # provider_idx
            if end_idx >= size_idx[i][1]:
                del provider_idx[i]
                end_idx = size_idx[i][1]

            mixed_adds = mixed_adds + adds[current_idx[i]:end_idx]
            current_idx[i] = end_idx

    return mixed_adds
