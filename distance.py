from math import sqrt


#Calculate the distance between 2 points
def _get_distance(point1, point2):
    if point2 is None:
        point2 = point1

    x_distance = point1[0] - point2[0]
    y_distance = point1[1] - point2[1]
    return sqrt(x_distance**2 + y_distance**2)


#Add the distance between 2 consecutive points and returns total distance
def get_total_distance(fish_trajectory):
    total_distance = 0
    for index in range(1, len(fish_trajectory)):
        #x1, y1 = fish_trajectory[index-1]
        #x2, y2 = fish_trajectory[index]
        
        # Add printout of compared coordinates
        #print(f"Comparing: ({x1}, {y1}) with ({x2}, {y2})")
        total_distance += _get_distance(fish_trajectory[index-1], fish_trajectory[index])
        
    return total_distance




# Function to calculate the speed in each time interval
def get_speed_over_time(fish_trajectory, times):
    speed_over_time = []
    for index in range(1, len(fish_trajectory)):
        distance_moved = _get_distance(fish_trajectory[index-1], fish_trajectory[index])
        time_interval = times[index] - times[index-1]
        if time_interval > 0:  # Avoid division by zero
            instant_speed = distance_moved / time_interval
            speed_over_time.append(instant_speed)
    return speed_over_time




# Function to calculate acceleration in each time interval
def get_acceleration_over_time(speed_over_time, times):
    acceleration_over_time = []
    for index in range(1, len(speed_over_time)):
        speed_change = abs(speed_over_time[index] - speed_over_time[index-1])
        time_interval = times[index] - times[index-1]
        if time_interval > 0:  # Avoid division by zero
            instant_acceleration = speed_change / time_interval
            acceleration_over_time.append(instant_acceleration)
    return acceleration_over_time