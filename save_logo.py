import base64
import os


def save_logo_from_base64(project_path, base64_string=""):
    # Decode the base64 string into binary data
    image_data = base64.b64decode(base64_string)

    # Define the path where you want to save the logo image
    logo_path = os.path.join(project_path, "app/src/main/res/drawable/ic_launcher.png")

    # Write the binary data to the image file
    with open(logo_path, "wb") as image_file:
        image_file.write(image_data)
        image_file.close()

    print("Logo saved successfully at:", logo_path)
    return logo_path
