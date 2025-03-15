from google.cloud import vision
import io

def detect_food(image_path):
    # Initialize the Vision API client
    client = vision.ImageAnnotatorClient()

    # Load the image file
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Create an Image object
    image = vision.Image(content=content)

    # Perform label detection
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # Extract and return food-related labels
    food_items = [label.description for label in labels if "food" in label.description.lower()]
    return food_items

# Example usage
if __name__ == "__main__":
    image_path = "pizza.jpg"  # Replace with the path to your image
    food_items = detect_food(image_path)
    print("Detected Food Items:", food_items)