import numpy as np

def simulate_porosity(depth, base_poro, lithology='sandstone', count=5, variability=5):
    """
    Generate realistic porosity array based on geology
    """
    # Depth compaction effect
    compaction_factor = np.exp(-0.0001 * depth)
    
    # Lithology constraints
    litho_ranges = {
        'sandstone': (15, 35),
        'carbonate': (5, 25),
        'shale': (1, 10),
        'granite': (0.1, 5),
        'basalt': (0.5, 8)
    }
    
    min_poro, max_poro = litho_ranges.get(lithology, (1, 35))
    base_poro = np.clip(base_poro * compaction_factor, min_poro, max_poro)
    
    # Generate samples with realistic distribution
    if lithology in ['shale', 'granite']:
        # Low porosity, lognormal distribution
        samples = np.random.lognormal(mean=np.log(base_poro), sigma=0.3, size=count)
    else:
        # Normal distribution for porous rocks
        samples = base_poro + np.random.normal(0, variability/3, size=count)
    
    return np.clip(samples, 0, 40)

def generate_environmental_data(depth, lithology):
    """
    Generate parameters for environmental applications
    """
    # Base parameters
    if lithology == 'sandstone':
        base_poro = np.random.uniform(20, 30)
        perm = np.random.uniform(100, 2000)
        contaminant_factor = np.random.uniform(0.1, 0.5)
    elif lithology == 'shale':
        base_poro = np.random.uniform(2, 8)
        perm = np.random.uniform(0.01, 1)
        contaminant_factor = np.random.uniform(0.8, 1.2)
    else:
        base_poro = np.random.uniform(10, 20)
        perm = np.random.uniform(10, 100)
        contaminant_factor = np.random.uniform(0.3, 0.7)
    
    return {
        'porosity': simulate_porosity(depth, base_poro, lithology),
        'permeability': perm,
        'contaminant_risk': contaminant_factor * depth / 1000
  }
