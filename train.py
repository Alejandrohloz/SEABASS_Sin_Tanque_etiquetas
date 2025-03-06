
from ultralytics import YOLO  # Import YOLO object detection model
import torch  # Import PyTorch for hardware acceleration

#YOLO model from scractch
model = YOLO('yolo11n.yaml')

#YOLO model for segmentation:
#model = YOLO('yolov8n-seg.pt')  #yolov8s-seg.pt

#pretrained YOLO model 
#model = YOLO('best.pt')

# Check if GPU is available; otherwise, default to CPU
device = "cuda" if torch.cuda.is_available() else "cpu"

device = "cpu"

# Train the model using the dataset defined in 'dataset.yaml'
# Training will run for 20 epochs on the selected device
results = model.train(data="dataset.yaml", epochs=20, device=device)