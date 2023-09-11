import cv2
import time
import sensehat

# Initialize the Sense Hat
sense = sensehat.SenseHat()

# Define the region of interest (ROI)
roi = (0, 0, 320, 240)

# Create a dictionary to store the Smarties colors
smarties_colors = {
    "blue": (0, 0, 255),
    "rose": (255, 0, 255),
    "green": (0, 255, 0),
    "red": (255, 0, 0),
    "yellow": (255, 255, 0),
    "purple": (128, 0, 128),
    "orange": (255, 165, 0),
    "brown": (165, 42, 42),
}

# Start a loop to capture images from the camera
while True:
    # Capture an image from the camera
    _, image = cv2.VideoCapture(0).read()

    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create masks for each of the Smarties colors
    masks = []
    for color, lower_bound, upper_bound in smarties_colors.items():
        lower_bound = np.array(lower_bound, dtype="uint8")
        upper_bound = np.array(upper_bound, dtype="uint8")
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
        masks.append(mask)

    # Find the Smarties in the image
    smarties = []
    for mask in masks:
        smarties.extend(cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0])

    # Keep track of the number of Smarties of each color
    smarties_count = {}
    for smartie in smarties:
        color = smarties_colors[min(smarties_colors, key=lambda x: cv2.mean(mask)[0])]
        if color not in smarties_count:
            smarties_count[color] = 0
        smarties_count[color] += 1

    # Display the color of the Smarties on the LED screen
    for color, count in smarties_count.items():
        sense.set_pixel(count, 0, smarties_colors[color])

    # Sleep for 1 second
    time.sleep(1)