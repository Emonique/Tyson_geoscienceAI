import numpy as np
from scipy.stats import entropy

def shannon_entropy(data, bins='auto', base=2):
    """Compute Shannon entropy with automatic binning"""
    hist, _ = np.histogram(data, bins=bins)
    probs = hist / np.sum(hist)
    probs = probs[probs > 0]
    return entropy(probs, base=base)

def tsallis_entropy(data, q=1.5, bins='auto'):
    """Compute Tsallis entropy for non-extensive systems"""
    hist, _ = np.histogram(data, bins=bins)
    probs = hist / np.sum(hist)
    probs = probs[probs > 0]
    
    if q == 1:
        return entropy(probs, base=np.e)
    else:
        return (1 - np.sum(probs**q)) / (q - 1)

def permutation_entropy(data, order=3, delay=1):
    """Compute permutation entropy for time-series/sequence data"""
    n = len(data)
    permutations = {}
    total = 0
    
    for i in range(n - (order - 1) * delay):
        # Get indices for the permutation
        idx = [i + j * delay for j in range(order)]
        segment = data[idx]
        # Create ordinal pattern
        pattern = tuple(np.argsort(segment))
        
        if pattern not in permutations:
            permutations[pattern] = 0
        permutations[pattern] += 1
        total += 1
    
    probs = np.array(list(permutations.values())) / total
    return entropy(probs, base=2) / np.log2(np.math.factorial(order))
