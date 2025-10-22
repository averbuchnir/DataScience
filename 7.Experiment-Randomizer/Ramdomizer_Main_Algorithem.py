import random
import numpy as np

def full_random_design(lines, treats, repetitions):
    """
    Generate a fully randomized experimental layout.

    This function allows unequal numbers of repetitions per Line–Treat combination.

    Parameters
    ----------
    lines : list[str]- like genotype names.
    treats : list[str] - lije Treatment names (e.g., control, drought).
    repetitions : int or dict[tuple[str, str], int]
        like:
          - a single integer (same repetition count for all), or
          - a dict mapping (line, treat) -> repetition count.
    Returns
    list[tuple[str, str, str]]
        Randomized list of (Label, Line, Treat).
    """

    all_combinations = []
    for line in lines:
        for treat in treats:
            # Determine repetition count for this specific combination
            if isinstance(repetitions, dict): 
                reps = repetitions.get((line, treat), 1)  # get the number of Rep for lineXTreat - Default to 1 if not specified
            else:
                reps = repetitions
            # Generate labels and add to the list
            for rep in range(reps):
                label = f"{line}_{treat}-{rep}" # create a unique label for each repetition
                all_combinations.append((label, line, treat)) # add to the list

    random.shuffle(all_combinations) # Randomize the order of all combinations
    return all_combinations


def block_design(lines, treats, repetitions):
    """
    Generate a randomized block design layout.

    Each block contains all Line×Treat combinations once.
    All treatments must have equal repetitions.

    Parameters
    ----------
    lines : list[str]- like genotype names.
    treats : list[str] - lije Treatment names (e.g., control, drought).
    repetitions : int or list[int]
        Number of repetitions (blocks). If list, all values must be equal.
    Returns
    -------
    list[tuple[str, str, str]]
        Randomized list of (Label, Line, Treat) across all blocks.

    Errors
    ------
    ValueError
        If block structure is inconsistent or repetitions are unequal.
    """

    # Handle list form for repetitions
    if isinstance(repetitions, list): # check for equality in repetitions
        if len(set(repetitions)) > 1: # more than one unique value
            raise ValueError("All treatments must have equal repetitions in Block Design.")
        repetitions = repetitions[0] # get the common repetition count - as they all are equal

    n_lines = len(lines) # number of lines
    n_treats = len(treats) # number of treatments
    total_expected = n_lines * n_treats * repetitions # total expected samples

    # One block = all possible Line×Treat combinations
    block = [(f"{line}_{treat}", line, treat) for line in lines for treat in treats] # create the block

    layout = [] # final layout list
    for r in range(repetitions):
        randomized_block = random.sample(block, len(block))  # Random order per block - shuffle the block
        for label, line, treat in randomized_block: 
            layout.append((f"{label}-{r}", line, treat)) # create unique label per repetition and add to layout

    if len(layout) != total_expected: 
        raise ValueError("Mismatch between Line×Treat×Repetition and generated layout.")

    return layout


# ---------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------

if __name__ == "__main__":

    lines = ["L1", "L2"] # example lines
    treats = ["T1", "T2"] # example treatments

    print("\n=== Full Random (Equal Reps) ===")
    layout_equal = full_random_design(lines, treats, 2) # equal repetitions
    for item in layout_equal:
        print(item)

    print("\n=== Full Random (Unequal Reps) ===")
    custom_reps = { # unequal repetitions example
        ("L1", "T1"): 3,
        ("L1", "T2"): 1,
        ("L2", "T1"): 2,
        ("L2", "T2"): 4
    }
    layout_unequal = full_random_design(lines, treats, custom_reps)
    for item in layout_unequal:
        print(item)

    print("\n=== Block Design (Valid) ===")
    layout_block = block_design(lines, treats, 6) # valid block design
    for item in layout_block:
        print(item)
    
    print("\n=== Block Design (Valid with List) ===")
    layout_block_list = block_design(lines, treats, [6 ,6]) # valid block design with list
    for item in layout_block_list:
        print(item)
        
    print("\n=== Block Design (Invalid) ===")
    try:
        layout_invalid = block_design(lines, treats, [2, 3]) # invalid block design`
    except ValueError as e:
        print("Error:", e,"\n\n")

