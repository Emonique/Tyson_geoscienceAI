import numpy as np
from scipy.stats import linregress

def compute_fractal_dimension(data, method='higuchi'):
    """
    Compute fractal dimension using efficient methods
    - 'higuchi': Fast 1D fractal dimension (default)
    - 'boxcount': Traditional box-counting
    """
    if method == 'higuchi':
        n = len(data)
        k_max = min(100, n // 10)  # Auto-adjust for small datasets
        
        L = []
        for k in range(1, k_max + 1):
            Lk = 0
            for m in range(k):
                idx = slice(m, None, k)
                segment = data[idx]
                if len(segment) > 1:
                    Lkm = np.sum(np.abs(np.diff(segment)))
                    norm_factor = (n - 1) / (k * ((n - m - 1) // k))
                    Lk += Lkm * norm_factor
            L.append(np.log(Lk / k) if Lk > 0 else 0)
        
        x = np.log(1 / np.arange(1, k_max + 1))
        valid = np.isfinite(L) & np.isfinite(x)
        if np.sum(valid) < 2:
            return 1.0  # Default for invalid cases
        slope, _, _, _, _ = linregress(x[valid], np.array(L)[valid])
        return abs(slope)
    
    elif method == 'boxcount':
        data_range = np.max(data) - np.min(data)
        if data_range == 0:
            return 0.0
            
        box_sizes = np.logspace(0, np.log10(data_range/2), 10, base=10)
        counts = []
        for size in box_sizes:
            if size <= 0:
                continue
            boxes = np.arange(np.min(data), np.max(data), size)
            count = 0
            for box in boxes:
                if np.any((data >= box) & (data < box + size)):
                    count += 1
            counts.append(count)
        
        log_sizes = np.log(1 / np.array(box_sizes[:len(counts)]))
        log_counts = np.log(counts)
        slope, _, _, _, _ = linregress(log_sizes, log_counts)
        return slope
    
    else:
        raise ValueError("Method must be 'higuchi' or 'boxcount'")
