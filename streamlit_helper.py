import streamlit as st
import requests
from PIL import Image


def introduction():
    """
    This function will display the introduction of the app.
    """
    st.title("What's in your fridge?")

    st.write(
        "This app will suggest a recipe based on the ingredients you have in your fridge. It will also provide you with a detailed list of steps to follow to cook it."
    )

    # Add a list of steps for the user to follow to get started

    st.write(
        "To get started, upload or take an photo of your fridge with your camera. Select an option from the menu."
    )


def input_image():
    """
    This function will display the menu to select the option to input the image.
    """
    # Add a menu to select the option
    option = st.selectbox(
        "Please select an option", ("Sample Image", "Upload", "Camera")
    )

    image = None
    if option == "Upload":
        uploaded_file = st.file_uploader(
            "Upload a picture of your fridge", type=["jpg"]
        )
        if uploaded_file is not None:
            image = Image.open(uploaded_file)

    elif option == "Camera":
        camera_photo = st.camera_input("Take a picture of your fridge")

        if camera_photo is not None:
            image = Image.open(camera_photo)

    elif option == "Sample Image":
        url = "https://static.toiimg.com/thumb/resizemode-4,width-1200,height-900,msid-67569905/67569905.jpg"
        image = Image.open(requests.get(url, stream=True).raw)

    return image
