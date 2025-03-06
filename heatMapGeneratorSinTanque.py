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
        self.grid_size = grid_size  # Tamaño de cada celda en la cuadrícula
        self.heatmap = np.zeros((height // grid_size, width // grid_size), dtype=np.float32)

    def add_positions(self, positions):
        """
        Agrega posiciones absolutas de los peces al heatmap.
        """
        for x, y in positions:
            grid_x = int(x // self.grid_size)
            grid_y = int(y // self.grid_size)

            if 0 <= grid_x < self.heatmap.shape[1] and 0 <= grid_y < self.heatmap.shape[0]:
                self.heatmap[grid_y, grid_x] += 1  # Incrementa la intensidad en la celda correspondiente
                
                
                
                
    def add_circle_to_heatmap(self, cx, cy, radius):
        """
        Dibuja un círculo que representa la ubicación del tanque en el heatmap.
        El círculo se dibuja en las celdas correspondientes dentro de la cuadrícula.
        """
        grid_cx = int(cx // self.grid_size)
        grid_cy = int(cy // self.grid_size)
        grid_radius = int(radius // self.grid_size)

        for i in range(max(0, grid_cx - grid_radius), min(self.heatmap.shape[1], grid_cx + grid_radius + 1)):
            for j in range(max(0, grid_cy - grid_radius), min(self.heatmap.shape[0], grid_cy + grid_radius + 1)):
                # Si la celda está dentro del círculo, incrementamos la intensidad
                if (i - grid_cx)**2 + (j - grid_cy)**2 <= grid_radius**2:
                    self.heatmap[j, i] += 1
                    
                    

    def generate_heatmap(self):
        """
        Genera y guarda el heatmap basado en las posiciones registradas.
        """
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

        plt.title("Heatmap - Movimiento de Peces")
        plt.xlabel("X (píxeles)")
        plt.ylabel("Y (píxeles)")

        # Guardar el heatmap
        plt.savefig(self.output_path, dpi=300, transparent=False)
        plt.close()
        print(f"Heatmap guardado en {self.output_path}")