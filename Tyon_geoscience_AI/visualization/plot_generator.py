import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
import os
from datetime import datetime

def generate_full_report(geo_memory, application='hydrocarbon'):
    """Generate comprehensive visual report"""
    plt.figure(figsize=(16, 12))
    gs = GridSpec(3, 3)
    
    # Application-specific title
    app_titles = {
        'hydrocarbon': 'Hydrocarbon Reservoir Analysis',
        'groundwater': 'Groundwater Resource Assessment',
        'contamination': 'Contaminant Transport Analysis',
        'geothermal': 'Geothermal Potential Assessment'
    }
    plt.suptitle(app_titles.get(application, 'Geoscience Analysis Report'), 
                fontsize=16, fontweight='bold')
    
    # Extract data
    depths = [d['depth'] for d in geo_memory]
    entropies = [d['entropy'] for d in geo_memory]
    fractal_dims = [d['fractal_dim'] for d in geo_memory]
    lithologies = [d['lithology'] for d in geo_memory]
    
    # Plot 1: Entropy vs Depth
    ax1 = plt.subplot(gs[0, 0])
    sc1 = ax1.scatter(depths, entropies, c=fractal_dims, cmap='viridis', s=50)
    ax1.set_title('Entropy vs Depth')
    ax1.set_xlabel('Depth (m)')
    ax1.set_ylabel('Shannon Entropy')
    plt.colorbar(sc1, ax=ax1, label='Fractal Dimension')
    
    # Plot 2: Fractal Dimension Distribution
    ax2 = plt.subplot(gs[0, 1])
    unique_litho = list(set(lithologies))
    colors = plt.cm.tab10(np.linspace(0, 1, len(unique_litho))
    
    for i, litho in enumerate(unique_litho):
        litho_dims = [fd for j, fd in enumerate(fractal_dims) 
                     if lithologies[j] == litho]
        ax2.hist(litho_dims, bins=10, alpha=0.7, color=colors[i], 
                label=litho, density=True)
    
    ax2.set_title('Fractal Dimension by Lithology')
    ax2.set_xlabel('Fractal Dimension')
    ax2.set_ylabel('Density')
    ax2.legend()
    
    # Plot 3: Application-specific visualization
    ax3 = plt.subplot(gs[0, 2])
    if application == 'hydrocarbon':
        rqis = [np.mean(d['rqi']) for d in geo_memory]
        ax3.scatter(depths, rqis, c=entropies, cmap='plasma', s=50)
        ax3.set_title('RQI vs Depth')
        ax3.set_ylabel('Mean RQI')
        plt.colorbar(sc3, ax=ax3, label='Entropy')
    
    elif application == 'groundwater':
        conductivities = [d.get('hydraulic_conductivity', 0) for d in geo_memory]
        ax3.scatter(depths, conductivities, c=entropies, cmap='plasma', s=50)
        ax3.set_title('Hydraulic Conductivity vs Depth')
        ax3.set_ylabel('K (m/s)')
        plt.colorbar(sc3, ax=ax3, label='Entropy')
    
    elif application in ['contamination', 'geothermal']:
        risks = [d.get('contaminant_risk', d.get('heat_capacity_ratio', 0)) 
                for d in geo_memory]
        ax3.scatter(depths, risks, c=entropies, cmap='plasma', s=50)
        ax3.set_title('Risk Profile' if application == 'contamination' 
                     else 'Heat Capacity Ratio')
        ax3.set_ylabel('Risk Score' if application == 'contamination' 
                      else 'Cp/Cv Ratio')
        plt.colorbar(sc3, ax=ax3, label='Entropy')
    
    # Plot 4: 3D-like projection
    ax4 = plt.subplot(gs[1, :], projection='3d')
    ax4.scatter(depths, entropies, fractal_dims, 
               c=depths, cmap='viridis', s=50)
    ax4.set_xlabel('Depth (m)')
    ax4.set_ylabel('Entropy')
    ax4.set_zlabel('Fractal Dim')
    ax4.set_title('Parameter Space Projection')
    
    # Plot 5: Confidence profile
    ax5 = plt.subplot(gs[2, 0])
    confidences = [d.get('confidence', 0) for d in geo_memory]
    ax5.plot(depths, confidences, 'o-', color='darkred')
    ax5.set_title('Trap/Resource Confidence')
    ax5.set_xlabel('Depth (m)')
    ax5.set_ylabel('Confidence')
    
    # Plot 6: Leak risk (environmental) or heat flow (geothermal)
    ax6 = plt.subplot(gs[2, 1:])
    if application in ['contamination', 'groundwater']:
        leak_risks = [d.get('leak_risk', False) for d in geo_memory]
        ax6.bar(depths, leak_risks, width=10, color='red')
        ax6.set_title('Leak Risk Zones')
        ax6.set_xlabel('Depth (m)')
        ax6.set_ylabel('Leak Risk')
    elif application == 'geothermal':
        temperatures = [d.get('temperature', 25) for d in geo_memory]
        ax6.plot(depths, temperatures, 'o-', color='orange')
        ax6.set_title('Temperature Profile')
        ax6.set_xlabel('Depth (m)')
        ax6.set_ylabel('Temperature (°C)')
    else:
        pressures = [d.get('pressure', 0) for d in geo_memory]
        ax6.plot(depths, pressures, 'o-', color='blue')
        ax6.set_title('Pressure Profile')
        ax6.set_xlabel('Depth (m)')
        ax6.set_ylabel('Pressure (MPa)')
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Save with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/{application}_analysis_{timestamp}.png"
    os.makedirs('reports', exist_ok=True)
    plt.savefig(filename, dpi=150)
    plt.close()
    
    return filename
