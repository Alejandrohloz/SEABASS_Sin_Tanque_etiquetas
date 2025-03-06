import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

# Create a colormap based on 'inferno' but with a white background
inferno = plt.get_cmap('inferno')
new_cmap = inferno(np.linspace(0, 1, 256))  # Get the color scale
new_cmap[0] = [1, 1, 1, 1]  # Change the first color (lowest value) to white (R=1, G=1, B=1, A=1)

# The new colormap
white_inferno = mcolors.ListedColormap(new_cmap)


# https://www.geeksforgeeks.org/matplotlib-pyplot-imshow-in-python/

class heatMapGenerator:
    def __init__(self, width, height, output_path, grid_size = 20):
        """
        Initialize the heatmap generator with the video frame size and output path.
        """
        self.width = width
        self.height = height
        self.output_path = output_path
        self.fish_relative_positions = []  # Store all detected fish relative positions
        self.tank_positions = []  # Store all detected tank positions
        self.initial_tank_position = None  # Fix the tank position from the first frame
        self.grid_size = grid_size  # Size of each grid cell into which the heatmap is divided
        
        #Create an empty matrix for the Heatmap based on the grid size
        self.heatmap = np.zeros((height // grid_size, width // grid_size), dtype=np.float32) 
        

    def set_tank_positions(self, tank_positions):
        """
        Store all detected tank positions (list of tuples: (x1, y1, x2, y2)).
        """
        self.tank_positions = tank_positions
        if self.tank_positions:
            self.initial_tank_position = self.tank_positions[0]  # Fix the tank in the first frame
        

    def add_positions(self, positions):
        """
        Add fish positions to be plotted in the heatmap.
        """
        self.fish_relative_positions.extend(positions)
        
        
        
    def generate_heatmap(self):
        """
        Generate and save a heatmap based on the recorded fish positions.
        """
        if not self.initial_tank_position:
            print("Error: No initial tank position is recorded.")
            return
        
        
        # Extract x1, y1, x2, y2 from th tank's bounding box (a rectangle)
        tank_x1, tank_y1, tank_x2, tank_y2 = self.initial_tank_position

        # Compute the center of the fixed tank
        tank_center_x = (tank_x1 + tank_x2) / 2
        tank_center_y = (tank_y1 + tank_y2) / 2

        
        for (fish_rel_x, fish_rel_y), (tank_x1, tank_y1, tank_x2, tank_y2) in zip(
            self.fish_relative_positions, self.tank_positions
        ):

            # Convert relative fish coordinates to absolute coordinates within the fixed tank space
            abs_x = int((tank_center_x + fish_rel_x) // self.grid_size)
            abs_y = int((self.height - (tank_center_y + fish_rel_y) - 1) // self.grid_size)  #Invert Y-axis. The Y coordinate in the video goes from top (0) to bottom.
            #abs_y = int((tank_center_y + fish_rel_y) // self.grid_size)  #If we change that Y coordinate in the video goes from bottom (0) to top.
            
            # Check if coordinates are within the valid heatmap range
            if 0 <= abs_x < self.heatmap.shape[1] and 0 <= abs_y < self.heatmap.shape[0]:
                self.heatmap[abs_y, abs_x] += 5 #Increment heatmap intensity at the fish position

        # Normalize heatmap values to range 0-255
        if self.heatmap.max() > 0:
            self.heatmap = (self.heatmap / self.heatmap.max()) * 255


        # Create a figure   
        fig, ax = plt.subplots(figsize=(10, 10)) 
        
        # Generate a heatmap with seaborn and apply the previous custom colormap
        sns.heatmap(self.heatmap, cmap=white_inferno, cbar=True, ax=ax, square=True,
                    xticklabels=True, yticklabels=True, cbar_kws={"label": "Fish Presence Frequency"})

        # Ensure axis ticks reach exactly the video width and height
        x_ticks = np.linspace(0, self.heatmap.shape[1] -1, num=11).astype(int)
        y_ticks = np.linspace(0, self.heatmap.shape[0] -1, num=11).astype(int)
        
        
        #Convert from cells to real pixels
        ax.set_xticks(x_ticks)
        ax.set_xticklabels((x_ticks * self.grid_size).astype(int))  
        ax.set_yticks(y_ticks)
        ax.set_yticklabels((y_ticks * self.grid_size).astype(int))  
        
        
        #Set axis limits to match video dimensions
        ax.set_xlim(0, self.width // self.grid_size -1)  
        ax.set_ylim(0, self.height // self.grid_size -1)  
        
        
        
        # Draw the tank as a circle
        tank_x1_grid = tank_x1 // self.grid_size
        tank_y1_grid = tank_y1 // self.grid_size
        tank_x2_grid = tank_x2 // self.grid_size
        tank_y2_grid = tank_y2 // self.grid_size
        
        radius_x = (tank_x2_grid - tank_x1_grid) / 2
        radius_y = (tank_y2_grid - tank_y1_grid) / 2
        
        # Adjust to prevent oval shape
        radius = max(radius_x, radius_y)  
        
        tank_center_x_grid = tank_center_x / self.grid_size
        tank_center_y_grid = (self.height - tank_center_y - 1) / self.grid_size
        #tank_center_y_grid = tank_center_y / self.grid_size   #If we change that Y coordinate in the video goes from bottom (0) to top.
        
        circle = plt.Circle((tank_center_x_grid, tank_center_y_grid), radius, color="yellow", fill=False, linewidth=2)
        ax.add_patch(circle)
        
        plt.plot(tank_center_x_grid, tank_center_y_grid, "y+") # Draw a yellow cross in the middle of the tank
        plt.plot(tank_center_x_grid, tank_center_y_grid, "yo") # Draw a yellow dot in the middle of the tank
        
        
        plt.title("Heatmap - Fish Movement Inside the Tank")
        plt.xlabel("X (pixels)")
        plt.ylabel("Y (pixels)")
        
        
        # Save the HeatMap
        plt.savefig(self.output_path, dpi=300, transparent=False)
        plt.close()
        print(f"Heatmap saved to {self.output_path}")
        
        
        
        
        
        
        
        
        