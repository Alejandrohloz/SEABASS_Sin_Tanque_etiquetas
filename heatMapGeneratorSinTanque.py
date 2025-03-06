import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

# Crear un colormap basado en 'inferno' pero con fondo blanco
inferno = plt.get_cmap('inferno')
new_cmap = inferno(np.linspace(0, 1, 256))  # Obtener la escala de colores
new_cmap[0] = [1, 1, 1, 1]  # Cambiar el primer color (valor más bajo) a blanco

# Nuevo colormap
white_inferno = mcolors.ListedColormap(new_cmap)


class heatMapGenerator:
    def __init__(self, width, height, output_path, grid_size=20):
        """
        Inicializa el generador de heatmap con el tamaño del video y la ruta de salida.
        """
        self.width = width
        self.height = height
        self.output_path = output_path
        self.fish_relative_positions = []  # Store all detected fish relative positions
        self.tank_mid_positions = []  # Store detected tank mid positions
        self.tank_radius_store = []  # Store detected tank radius
        self.grid_size = grid_size  # Tamaño de cada celda en la cuadrícula
        
        #Create an empty matrix for the Heatmap based on the grid size
        self.heatmap = np.zeros((height // grid_size, width // grid_size), dtype=np.float32)
        
    
    def set_tank_mid_positions(self, tank_mid_positions):
        """
        Set tank mid positions from detected tanks (list of tuples: (x, y)).
        """
        self.tank_mid_positions = tank_mid_positions
        
        
        
    def set_tank_radius_store(self, tank_radius_store):
        """
        Set tank radii from detected tanks.
        """
        self.tank_radius_store = tank_radius_store
        
            

    def add_positions(self, positions):
        """
        Add fish relative positions to be plotted in the heatmap.
        """
        self.fish_relative_positions.extend(positions)
                
                
                    
                    

    def generate_heatmap(self):
        """
        Genera y guarda el heatmap basado en las posiciones registradas.
        """
        
        
        if not self.fish_relative_positions:
            print("Error: No fish positions recorded.")
            return
        
        
        # Increment heatmap intensity based on fish positions
        for (fish_rel_x, fish_rel_y) in self.fish_relative_positions:
            abs_x = int(fish_rel_x // self.grid_size)
            abs_y = int((self.height - fish_rel_y) // self.grid_size)  # Inverted Y-axis

            # Check if coordinates are within the valid heatmap range
            if 0 <= abs_x < self.heatmap.shape[1] and 0 <= abs_y < self.heatmap.shape[0]:
                self.heatmap[abs_y, abs_x] += 1  # Increment heatmap intensity at the fish position
                
                

        if self.heatmap.max() > 0:
            self.heatmap = (self.heatmap / self.heatmap.max()) * 255  # Normalizar entre 0 y 255

        fig, ax = plt.subplots(figsize=(10, 10))
        sns.heatmap(self.heatmap, cmap=white_inferno, cbar=True, ax=ax, square=True,
                    xticklabels=True, yticklabels=True, cbar_kws={"label": "Frecuencia de Presencia de Peces"})

        # Etiquetas de ejes en píxeles reales
        x_ticks = np.linspace(0, self.heatmap.shape[1] - 1, num=11).astype(int)
        y_ticks = np.linspace(0, self.heatmap.shape[0] - 1, num=11).astype(int)

        ax.set_xticks(x_ticks)
        ax.set_xticklabels((x_ticks * self.grid_size).astype(int))
        ax.set_yticks(y_ticks)
        ax.set_yticklabels((y_ticks * self.grid_size).astype(int))

        ax.set_xlim(0, self.width // self.grid_size - 1)
        ax.set_ylim(0, self.height // self.grid_size - 1)
        
        
        # Draw the tank as a circle if available
        if self.tank_mid_positions and self.tank_radius_store:
            for (tank_x, tank_y), radius in zip(self.tank_mid_positions, self.tank_radius_store):
                radius_cells = radius // self.grid_size  # Convert radius to grid cells
                tank_center_x_grid = tank_x // self.grid_size
                tank_center_y_grid = (self.height - tank_y) // self.grid_size  # Inverted Y-axis
                
                # Adjust to prevent oval shape
                circle = plt.Circle((tank_center_x_grid, tank_center_y_grid), radius_cells, color="yellow", fill=False, linewidth=2)
                ax.add_patch(circle)
                ax.plot(tank_center_x_grid, tank_center_y_grid, "y+")  # Draw a yellow cross in the middle of the tank
                ax.plot(tank_center_x_grid, tank_center_y_grid, "yo")  # Draw a yellow dot in the middle of the tank

        plt.title("Heatmap - Movimiento de Peces")
        plt.xlabel("X (píxeles)")
        plt.ylabel("Y (píxeles)")

        # Guardar el heatmap
        plt.savefig(self.output_path, dpi=300, transparent=False)
        plt.close()
        print(f"Heatmap guardado en {self.output_path}")