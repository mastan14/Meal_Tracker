from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

# Initialize the Clarifai client
def initialize_clarifai_client(api_key):
    """
    Initialize the Clarifai client using the API key.
    """
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', f'Key {api_key}'),)
    return stub, metadata

# Predict food items in an image
def predict_food_items(stub, metadata, image_path):
    """
    Use the Clarifai Food Model to predict food items in an image.
    """
    try:
        # Read the image file
        with open(image_path, "rb") as f:
            file_bytes = f.read()

        # Create a request for the Food model
        request = service_pb2.PostModelOutputsRequest(
            model_id="bd367be194cf45149e75f01d59f77ba7",  # Clarifai Food Model ID
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=file_bytes
                        )
                    )
                )
            ]
        )

        # Send the request to the Clarifai API
        response = stub.PostModelOutputs(request, metadata=metadata)

        # Check if the request was successful
        if response.status.code != status_code_pb2.SUCCESS:
            raise Exception(f"Request failed with status {response.status.description}")

        # Extract predictions
        predictions = response.outputs[0].data.concepts
        return predictions

    except Exception as e:
        print(f"Error predicting food items: {e}")
        return None