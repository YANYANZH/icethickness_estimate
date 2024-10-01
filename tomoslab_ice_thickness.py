"""This program will take in a simplified refinment star file, and based on the particle position 
in each tomogram to estimate the icethickness of the each particle. The outputs are icethickness average, distribution, 
and thickness discription txt file"""

import numpy as np

# Specify the path to your text file
file_path = 'xx'  # Replace with your file's path
# Specify the path to the output text file
output_file = 'xxthickness.txt'

# Define the number of bins for the XY plane
num_x_bins = 5
num_y_bins = 5

def calculate_slab_thickness(pts):
    # Replace these points with your XYZ coordinates
    points = [t[:3] for t in pts]
    points = np.array(points)
    pts = np.array(pts)

    # Extract X, Y, and Z coordinates from the points
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    ptcl = pts[:, 3]


    # Add an extra column initialized with zeros
    pts_new = np.column_stack((x, y, z, ptcl, np.zeros_like(x)))  

    # Divide the XY plane into bins and find the points with the largest and smallest Z values in each bin
    x_bin_edges = np.linspace(min(x), max(x), num_x_bins + 1)
    y_bin_edges = np.linspace(min(y), max(y), num_y_bins + 1)

    largest_z_values = np.zeros((num_x_bins, num_y_bins))
    smallest_z_values = np.ones((num_x_bins, num_y_bins))  # Initialize with a high value
    Z_diff = []
    for i in range(num_x_bins):
        for j in range(num_y_bins):
            x_min = x_bin_edges[i]
            x_max = x_bin_edges[i + 1]
            y_min = y_bin_edges[j]
            y_max = y_bin_edges[j + 1]
            

            mask = (x >= x_min) & (x < x_max) & (y >= y_min) & (y < y_max)

            if np.any(mask):
                max_z_in_bin = np.max(z[mask])
                min_z_in_bin = np.min(z[mask])
                largest_z_values[i, j] = max_z_in_bin
                smallest_z_values[i, j] = min_z_in_bin

                # Calculate the difference between the largest and smallest Z values in each bin
                z_difference = max_z_in_bin - min_z_in_bin
                
                # Set z_difference for all points in this bin
                pts_new[mask, 4] = z_difference  # Assuming the 5th column for z_difference
                pts_update = [tuple(row) for row in pts_new]
                Z_diff.append(z_difference) 

    Z_diff_avg = np.mean(Z_diff)
    return Z_diff, Z_diff_avg, pts_update




# Initialize an empty dictionary to store the coordinates by tomo
tomo_slabs = {}

# Open the file in read mode
with open(file_path, 'r') as file:
    # Read each line in the file
    for line in file:
        point = line.strip().split()
        # Split the line into x, y, and z components
        x, y, z= map(float, point[:3])
        ptcl = point[-2]
        # Create a tuple and append it to the list
        coordinate = (x, y, z, ptcl)
        slab = point[-1]
        if slab not in tomo_slabs:
            tomo_slabs[slab] = []
        tomo_slabs[slab].append(coordinate)
    
    # Compute the thickness of tomograms
    slabs_z_difference = {} 
    slabs_z_diff_avg = []
    count = 0
    for slab,pts in tomo_slabs.items():
        Z_diff, Z_diff_avg, pts_update = calculate_slab_thickness(pts)
        slabs_z_difference[slab] = Z_diff
        slabs_z_diff_avg.append(Z_diff_avg)
        tomo_slabs[slab] = pts_update
        count += 1

    # Open the file for writing
    with open(output_file, 'w') as file:
        # Write the header row with column names
        file.write('TS\X\Y\Z\PTCL\THICKNESS\n')

        # Iterate through the dictionary and write each key-value pair
        for tomo, slab in tomo_slabs.items():

            # Write each value in the tuple into separate columns
            for ptcl in slab:
                for value in ptcl:
                    file.write(f'{value}\t')
                file.write('\n')

    print(f'Dictionary has been written to {output_file}')


        


            


        