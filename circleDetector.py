import cv2
import numpy as np

class circleDetector:
    def __init__(self, min_radius=30, max_radius=400):
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.tank_coords = None  # Guardar las coordenadas del centro del círculo (tanque)
        self.tank_radius = None  # Guardar el radio del círculo (tanque)
    
    def process_frame(self, frame):
        # Convierte el fotograma a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplica un desenfoque para reducir ruido
        gray_blurred = cv2.blur(gray, (3, 3))

        # Aplica la transformada de Hough para detectar círculos
        detected_circles = cv2.HoughCircles(
            gray_blurred,
            cv2.HOUGH_GRADIENT,
            1,
            20,
            param1=50,
            param2=30,
            minRadius=self.min_radius,
            maxRadius=self.max_radius
        )

        # Si se detectan círculos, dibuja el primero
        if detected_circles is not None:
            # Convierte los parámetros de los círculos (a, b, r) a enteros
            detected_circles = np.uint16(np.around(detected_circles))

            # Selecciona solo el primer círculo detectado
            a, b, r = detected_circles[0][0]  # El primer círculo detectado
            
            # Guarda las coordenadas del centro del círculo (tanque) y el radio
            self.tank_coords = (a, b)
            self.tank_radius = r

            # Dibuja la circunferencia del primer círculo
            cv2.circle(frame, (a, b), r, (0, 255, 0), 2)

            # Dibuja un pequeño círculo (de radio 1) para mostrar el centro
            cv2.circle(frame, (a, b), 1, (0, 0, 255), 3)
            
        else:
            self.tank_coords = None
            self.tank_radius = None
            print("No se detectó un círculo (tanque).")

        return frame

    def get_tank_info(self):
        # Retorna las coordenadas y el radio del tanque
        return self.tank_coords, self.tank_radius