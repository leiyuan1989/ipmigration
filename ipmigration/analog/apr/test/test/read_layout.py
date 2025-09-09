import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import Dict, List

# --------------------------
# Step 1: Original Data Extraction (Unmodified, Ensures Correct Fields)
# --------------------------
def extract_layout_data(file_path: str) -> Dict[str, List[Dict]]:
    """
    Extract full layout data (pmos, nmos, mimcap, rnhpoly, vias) with shortened fields (LLX, LLY, URX, URY).
    Returns structured data ready for visualization.
    """
    data: Dict[str, List[Dict]] = {
        "pmos": [],
        "nmos": [],
        "mimcap": [],
        "rnhpoly": [],
        "vias": []
    }
    
    vias_count = 1
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped_line = line.strip()
            if not stripped_line:
                continue
            parts = stripped_line.split()

            # Extract PMOS (M-prefix + pmos3v)
            if len(parts) >= 11 and parts[0].startswith('M') and parts[1] == 'pmos3v':
                data["pmos"].append({
                    "Comp_Name": parts[0],
                    "Type": parts[1],
                    "LLX": float(parts[2]),
                    "LLY": float(parts[3]),
                    "URX": float(parts[4]),
                    "URY": float(parts[5]),
                    "X": float(parts[6]),
                    "Y": float(parts[7]),
                    "Rotate": parts[8],
                    "Length": parts[9],
                    "Width": parts[10]
                })

            # Extract NMOS (M-prefix + nmos3v)
            elif len(parts) >= 11 and parts[0].startswith('M') and parts[1] == 'nmos3v':
                data["nmos"].append({
                    "Comp_Name": parts[0],
                    "Type": parts[1],
                    "LLX": float(parts[2]),
                    "LLY": float(parts[3]),
                    "URX": float(parts[4]),
                    "URY": float(parts[5]),
                    "X": float(parts[6]),
                    "Y": float(parts[7]),
                    "Rotate": parts[8],
                    "Length": parts[9],
                    "Width": parts[10]
                })

            # Extract MIM Capacitor (C-prefix + mimcap)
            elif len(parts) >= 11 and parts[0].startswith('C') and parts[1] == 'mimcap':
                data["mimcap"].append({
                    "Comp_Name": parts[0],
                    "Type": parts[1],
                    "LLX": float(parts[2]),
                    "LLY": float(parts[3]),
                    "URX": float(parts[4]),
                    "URY": float(parts[5]),
                    "X": float(parts[6]),
                    "Y": float(parts[7]),
                    "Rotate": parts[8],
                    "Length": parts[9],
                    "Width": parts[10]
                })

            # Extract rnhpoly Resistor (R-prefix + rnhpoly)
            elif len(parts) >= 12 and parts[0].startswith('R') and parts[1] == 'rnhpoly':
                data["rnhpoly"].append({
                    "Comp_Name": parts[0],
                    "Type": parts[1],
                    "LLX": float(parts[2]),
                    "LLY": float(parts[3]),
                    "URX": float(parts[4]),
                    "URY": float(parts[5]),
                    "X": float(parts[6]),
                    "Y": float(parts[7]),
                    "Rotate": parts[8],
                    "Length": parts[9],
                    "Width": parts[10],
                    "Segments": int(parts[11])
                })

            # Extract Vias (retained but filtered later)
            elif len(parts) >= 9 and parts[0] == 'vias':
                data["vias"].append({
                    "Comp_Name": f"vias_{vias_count}",
                    "Via_Type": parts[1],
                    "LLX": float(parts[2]),
                    "LLY": float(parts[3]),
                    "URX": float(parts[4]),
                    "URY": float(parts[5]),
                    "Rotate": parts[6],
                    "Rows": int(parts[7]),
                    "Cols": int(parts[8])
                })
                vias_count += 1

    return data

# --------------------------
# Step 2: Corrected Visualization Function (Input: layout_data)
# --------------------------
def plot_non_vias_components(layout_data: Dict[str, List[Dict]], save_path: str = "non_vias_layout.png"):
    """
    Plot all components EXCEPT vias from layout_data.
    Fixed Issue: Uses comp["URX"] and comp["URY"] (not undefined variable URX/URY).
    """
    # Initialize plot
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(18, 14))  # Large canvas for clarity

    # Style mapping for different component types (color, line width, legend label)
    comp_styles = {
        "pmos":      {"color": "#2E86AB", "edgewidth": 2, "label": "PMOS (M-prefix)"},
        "nmos":      {"color": "#A23B72", "edgewidth": 2, "label": "NMOS (M-prefix)"},
        "mimcap":    {"color": "#F18F01", "edgewidth": 3, "label": "MIM Cap (C-prefix)"},
        "rnhpoly":   {"color": "#C73E1D", "edgewidth": 3, "label": "RNHPoly Res (R-prefix)"}
    }

    # Collect all non-vias component types (exclude "vias" key)
    non_vias_types = [ct for ct in layout_data.keys() if ct != "vias"]
    all_coords = []  # For auto-fitting axis limits

    # Plot each non-vias component
    for comp_type in non_vias_types:
        components = layout_data[comp_type]
        if not components:
            continue  # Skip empty component types
        
        style = comp_styles[comp_type]
        for comp in components:
            # Get box coordinates from component dictionary (FIXED: comp["URX"] instead of URX)
            llx = comp["LLX"]
            lly = comp["LLY"]
            urx = comp["URX"]  # Use lowercase variable for clarity (matches field name)
            ury = comp["URY"]
            width = urx - llx
            height = ury - lly

            # Draw component box (outline only, no fill)
            rect = patches.Rectangle(
                (llx, lly),          # Bottom-left corner (LLX, LLY)
                width, height,       # Box dimensions (URX-LLX, URY-LLY)
                linewidth=style["edgewidth"],
                edgecolor=style["color"],
                facecolor='none'     # Transparent to avoid blocking other components
            )
            ax.add_patch(rect)

            # Add component name label (centered in the box)
            label_x = llx + width / 2
            label_y = lly + height / 2
            ax.text(
                label_x, label_y,
                comp["Comp_Name"],
                ha='center', va='center',  # Align text to box center
                fontsize=9,
                color=style["color"],
                fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.7)  # White background for readability
            )

            # Collect coordinates for auto-fitting axes (FIXED: use comp["URX"]/comp["URY"])
            all_coords.extend([(llx, lly), (urx, ury)])

    # --------------------------
    # Plot Customization
    # --------------------------
    # Axis labels and title
    ax.set_xlabel("X Coordinate (μm)", fontsize=12, fontweight='bold', labelpad=10)
    ax.set_ylabel("Y Coordinate (μm)", fontsize=12, fontweight='bold', labelpad=10)
    ax.set_title("IC Layout: Non-Vias Components (PMOS/NMOS/MIMCap/RNHPoly)", 
                 fontsize=16, fontweight='bold', pad=20)

    # Legend (distinguish component types)
    ax.legend(loc='upper right', fontsize=11, frameon=True, fancybox=True, shadow=True)

    # Grid for coordinate reference
    ax.grid(True, alpha=0.3, linestyle='--', color='gray')

    # Auto-fit axis limits (add 5% margin to prevent component cutoff)
    if all_coords:
        all_x = [coord[0] for coord in all_coords]
        all_y = [coord[1] for coord in all_coords]
        x_margin = (max(all_x) - min(all_x)) * 0.05
        y_margin = (max(all_y) - min(all_y)) * 0.05
        ax.set_xlim(min(all_x) - x_margin, max(all_x) + x_margin)
        ax.set_ylim(min(all_y) - y_margin, max(all_y) + y_margin)

    # Ensure no box distortion (equal aspect ratio)
    ax.set_aspect('equal', adjustable='box')

    # Save and display plot
    plt.tight_layout()  # Fix spacing to avoid label cutoff
    plt.savefig(save_path, dpi=300, bbox_inches='tight')  # High resolution (300 DPI)
    plt.show()

    # Print summary
    total_non_vias = sum(len(layout_data[ct]) for ct in non_vias_types)
    print(f"Plot saved to: {save_path}")
    print(f"Plotted {total_non_vias} non-vias components (vias excluded).")

# --------------------------
# Step 3: Main Workflow (Extract → Plot)
# --------------------------
if __name__ == "__main__":
    # Configuration (update paths to match your file location)
    INPUT_FILE = "layout_data.txt"       # Path to your layout data file
    OUTPUT_PLOT = "non_vias_layout.png"  # Path to save the final plot

    # 1. Extract full layout data (including vias)
    print(f"extracting full layout data from {INPUT_FILE}...")
    layout_data = extract_layout_data(INPUT_FILE)

    # 2. Validate non-vias data exists
    non_vias_count = sum(len(layout_data[ct]) for ct in layout_data.keys() if ct != "vias")
    if non_vias_count == 0:
        print("Error: No non-vias components found in layout_data. Check your input file.")
    else:
        # 3. Plot non-vias components (input: layout_data)
        print(f"Found {non_vias_count} non-vias components. Generating plot...")
        plot_non_vias_components(layout_data, OUTPUT_PLOT)