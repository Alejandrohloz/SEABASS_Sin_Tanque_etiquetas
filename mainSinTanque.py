import pyautogui  # Para obtener el tamaño de la pantalla
import os
from ultralytics import YOLO
import cv2
import pandas as pd
import matplotlib.pyplot as plt  # Para graficar los resultados
from pathlib import Path
import torch  # Para aceleración por hardware

import heatMapGeneratorSinTanque
import circleDetector
import distance
import textVideo



# Crear el directorio de salida
output_dir = Path(f'output')
output_dir.mkdir(exist_ok=True)

charts_dir = Path(f'{output_dir.name}/charts')
charts_dir.mkdir(exist_ok=True)

# Obtener el tamaño de la pantalla
screen_width, screen_height = pyautogui.size()

device = "cuda" if torch.cuda.is_available() else "cpu"

model_path = 'last.pt'  # Ruta al modelo entrenado
model_path = r"W:\HectorGarciaPalencia\lubinas_app\best_model\last.pt"
model = YOLO(model_path).to(device)

video_path = 'videos/Video_Prueba_2.mp4'  # Ruta del video
cap = cv2.VideoCapture(video_path)

# Rutas para guardar los archivos de salida
output_path = 'output/processed_video.mp4'
output_text_path = 'output/total_distance.txt'
output_positions_path = 'output/charts/fish_positions.xlsx'
output_speed_path = 'output/charts/speed_overtime.png'
output_acceleration_path = 'output/charts/acceleration_overtime.png'
output_heatMap_path = 'output/charts/fish_heatmap.png'

# Obtener el tamaño del video original
original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Configurar el archivo de video de salida
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para .mp4
out = cv2.VideoWriter(output_path, fourcc, fps, (original_width, original_height))

# Función para obtener el centro del bounding box
def get_middle(x1, y1, x2, y2):
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    return cx, cy

#Instantiate CircleDetector
circle_detector = circleDetector.circleDetector(min_radius=30, max_radius=400)

# Variables para almacenar las trayectorias del pez
fish_trajectory = []
fish_total_trajectory = []

fish_absolute_positions = []
fish_relative_positions = []
fish_positions = []
times = [0]

frame_count = 0  # Contador de frames
max_distance = 50.  # Para evitar detectar reflejos como movimientos del pez

tank_mid_positions = []
tank_radius_store = []

# Procesar los frames del video
while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(source=frame, save=False)  # Realizar predicción con el modelo

    # Dibuja las cajas de detección y las etiquetas
    annotated_frame = results[0].plot()

    fish_coords = None  # Coordenadas del pez
    tank_coords = None  #Coordenadas del tanque

    # Procesar las detecciones
    for box in results[0].boxes.data:
        x1, y1, x2, y2, conf, cls = box.cpu().numpy()  # Coordenadas de la caja (xmin, ymin, xmax, ymax)
        label = model.names[int(cls)]  # Nombre de la clase

        if label == 'fish':
            fish_coords = (x1, y1, x2, y2)
            
    # Procesar el frame para detectar el tanque
    annotated_frame = circle_detector.process_frame(annotated_frame)
        
    # Obtener las coordenadas del tanque  (detectadas como círculos) y su radio
    tank_coords, tank_radius = circle_detector.get_tank_info()    

    if fish_coords:
        # Coordenadas del pez (centro de la caja)
        cx_fish, cy_fish = get_middle(*fish_coords)
        
        fish_absolute_positions.append((cx_fish, cy_fish))

        # Ignorar saltos irrealistas debido a reflejos
        if fish_total_trajectory:
            last_position = fish_total_trajectory[-1]  # Última posición registrada
            distance_moved = distance._get_distance((cx_fish, cy_fish), last_position)

            if distance_moved > max_distance:
                print(f"Movimiento muy grande detectado ({distance_moved:.2f} px). Ignorando el frame.")
                continue  # Ignorar este frame si el salto es irrealista

        # Almacenar la trayectoria total del pez
        fish_total_trajectory.append((cx_fish, cy_fish))    
        fish_trajectory.append((cx_fish, cy_fish))

        # Limitar la historia de la trayectoria a los últimos 150 frames
        if len(fish_trajectory) > 150:
            fish_trajectory.pop(0)

        # Dibujar la trayectoria sobre el frame
        for i in range(1, len(fish_trajectory)):
            cv2.line(annotated_frame, 
                    (int(fish_trajectory[i-1][0]), int(fish_trajectory[i-1][1])), 
                    (int(fish_trajectory[i][0]), int(fish_trajectory[i][1])), 
                    color=(255, 0, 0), thickness=2)   

    # Si tenemos las coordenadas del tanque, calculamos las relativas del pez
    if tank_coords and fish_coords:
        # Obtener el centro del tanque
        cx_tank, cy_tank = tank_coords
        tank_mid_positions.append(tank_coords)
        tank_radius_store.append(tank_radius)
        
        # Calcular la posición relativa respecto al tanque
        relative_x = cx_fish - cx_tank
        relative_y = cy_fish - cy_tank
        
        fish_relative_positions.append((relative_x, relative_y))
        
        # Mostrar las coordenadas relativas sobre el frame
        textVideo.write_text_on_video(annotated_frame, relative_x, relative_y)
        
        # Guardar las posiciones y las posiciones relativas con el número de frame
        fish_positions.append({'Frame': frame_count, 'X': cx_fish, 'Y': cy_fish, 'Xrelative': relative_x, 'Yrelative': relative_y, 'XTank':cx_tank, 'YTank':cy_tank})
        frame_count += 1  # Incrementar contador de frames
        times.append(frame_count / fps)  # Tiempo real = frame / fps
        
    #Dibujar el circulo del tanque en el fotograma    
    annotated_frame = circle_detector.process_frame(annotated_frame)

    # Redimensionar el frame para ajustarse a la pantalla
    scale_factor = min(screen_width / annotated_frame.shape[1], screen_height / annotated_frame.shape[0])
    new_width = int(annotated_frame.shape[1] * scale_factor)
    new_height = int(annotated_frame.shape[0] * scale_factor)
    resized_frame = cv2.resize(annotated_frame, (new_width, new_height))

    # Mostrar el frame con anotaciones
    cv2.imshow('Press Q to exit', resized_frame)

    # Escribir el frame procesado en el video de salida
    out.write(annotated_frame)

    # Salir si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cálculos y gráficos
total_distance = distance.get_total_distance(fish_total_trajectory)
print(f"Distancia total del pez: {total_distance:.2f} píxeles")

if len(fish_trajectory) > 1 and len(times) > 1:
    speed_over_time = distance.get_speed_over_time(fish_total_trajectory, times)
    if len(speed_over_time) > 1:
        acceleration_over_time = distance.get_acceleration_over_time(speed_over_time, times)
    else:
        acceleration_over_time = []

# Guardar la distancia total en un archivo de texto
with open(output_text_path, 'w') as f:
    f.write(f"Distancia total del pez: {total_distance:.2f} píxeles\n")

# Guardar todas las posiciones en un archivo Excel
df = pd.DataFrame(fish_positions)  # Convertir la lista en DataFrame
df.to_excel(output_positions_path, index=False)  # Guardar como Excel

# Graficar la velocidad a lo largo del tiempo
if speed_over_time:
    time_axis = times[:len(speed_over_time)]
    plt.figure()
    plt.plot(time_axis, speed_over_time, linestyle='-', label=f'Pez', color=(0, 0, 1))
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Velocidad (píxeles/s)')
    plt.title('Velocidad a lo largo del tiempo')
    plt.grid(True)
    plt.legend()
    plt.savefig(output_speed_path, dpi=300)

# Graficar la aceleración a lo largo del tiempo
if acceleration_over_time:
    time_axis = times[:len(acceleration_over_time)]
    plt.figure()
    plt.plot(time_axis, acceleration_over_time, linestyle='-', label=f'Pez', color=(0, 0, 1))
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Aceleración (píxeles/s^2)')
    plt.title('Aceleración a lo largo del tiempo')
    plt.grid(True)
    plt.legend()
    plt.savefig(output_acceleration_path, dpi=300)
    

#HEATMAP    
heatmap_generator = heatMapGeneratorSinTanque.heatMapGenerator(original_width, original_height, output_heatMap_path)

# Set the tank coordinates (x, y)
if tank_coords:
    heatmap_generator.set_tank_mid_positions(tank_mid_positions)
    heatmap_generator.set_tank_radius_store(tank_radius_store)
    
# Add recorded fish positions
heatmap_generator.add_positions(fish_relative_positions)

# Agregar el círculo de radio al generador de mapas de calor
if tank_coords and tank_radius:
    cx_tank, cy_tank = tank_coords
    # Por ejemplo, agregar un círculo (de radio) al mapa de calor
    #heatmap_generator.add_circle_to_heatmap(cx_tank, cy_tank, tank_radius)
    

# Generar el mapa de calor aqui debe dibujar tambienel circulo con el radio y los centros para las coordenadas relativas del pez y eso
heatmap_generator.generate_heatmap() 

# Liberar recursos
cap.release()
out.release()
cv2.destroyAllWindows()