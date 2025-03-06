import cv2

#cv2.putText(image, text, (x, y), font, font_size, color, thickness)
            #ejes
            #        -
            #    -       + 
            #        +

"""
    This method has the function of adding text in the output video
"""
def write_text_on_video(annotated_frame, relative_x, relative_y):
    
    cv2.putText(annotated_frame, 
                        "Relative Position of the Fish in relation to the center of the Tank (x, y):", 
                        (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.8, 
                        color=(0, 255, 0), 
                        thickness=2)
            
    cv2.putText(annotated_frame, 
                        f"({relative_x:.2f}, {relative_y:.2f})", 
                        (60, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.8, 
                        color=(0, 255, 0), 
                        thickness=2)

    cv2.putText(annotated_frame, 
                        "AXIS:", 
                        (20, 150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.8, 
                        color=(0, 255, 0), 
                        thickness=2)

    cv2.putText(annotated_frame, 
                        "X: + (Right), - (Left)", 
                        (60, 180), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.8, 
                        color=(0, 255, 0), 
                        thickness=2)
    
    cv2.putText(annotated_frame, 
                        "Y: + (Down),   - (Up)", 
                        (60, 210), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.8, 
                        color=(0, 255, 0), 
                        thickness=2)
    
    #If we change that Y coordinate in the video goes from bottom (0) to top.
    """
    cv2.putText(annotated_frame, 
                        "Y: + (Up),     - (Down)", 
                        (60, 210), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.8, 
                        color=(0, 255, 0), 
                        thickness=2)
    """