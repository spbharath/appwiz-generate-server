# importing the module
import shutil
import os
import time
import random
import string
from tempfile import TemporaryDirectory
import xml.etree.ElementTree as ET

from flask import app
from customemailgen import send_email
import pymongo
import base64
from save_logo import save_logo_from_base64


def createTempDir(app_name, username, template_path, app_image):

    try:

        with TemporaryDirectory(dir="/home/valli/testing") as tmp:

            print("Created", tmp)
            base_src_path = "/home/valli/testing/Project"

            if copyDirectory(base_src_path, tmp):

                print("Copied BaseProject to TempDirectory")
                template_src_path = template_path  # "/home/valli/testing/Templates/Education/template_1"
                template_dest_path = tmp + "/BaseAndroidProject/app/src/main/assets/"

                if changeTemplate(template_src_path, template_dest_path, app_name):
                    print("Copied Templates to BaseProject in TempDirectory")
                    logo_prjt_path = tmp + "/BaseAndroidProject"
                    print(app_image)
                    if save_logo_from_base64(logo_prjt_path, base64_string=app_image):
                        if editAppName(tmp, app_name):
                            print("Changed Appname to " + app_name)
                            print("Generating APK...........")
                            app_storage_path = "/home/valli/testing/apps/"
                            app_name_format = f"Appify_{username}_{app_name}"
                            temp_apps_path = tmp + "/appify_apps/"
                            apk = False
                            aab = False
                            if runApkGeneration(tmp):
                                generated_app_path = (
                                    tmp
                                    + "/BaseAndroidProject/app/build/outputs/apk/customRelease/app-customRelease.apk"
                                )
                                apk_path = temp_apps_path + app_name_format + ".apk"
                                shutil.move(generated_app_path, apk_path)
                                os.chdir("/home/valli/testing")
                                print("Generated APK copied to the apps bin")
                                apk = True
                            else:
                                print("Error : Apk Generation Failed!")
                            if runAabGeneration(tmp):
                                generated_app_path = (
                                    tmp
                                    + "/BaseAndroidProject/app/build/outputs/bundle/release/app-release.aab"
                                )
                                aab_path = temp_apps_path + app_name_format + ".aab"
                                shutil.move(generated_app_path, aab_path)
                                os.chdir("/home/valli/testing")
                                print("Generated AAB copied to the apps bin")
                                aab = True
                            else:
                                print("Error : AAB Generation Failed!")
                            if apk and aab:
                                random_string = "".join(
                                    random.choice(string.ascii_letters + string.digits)
                                    for _ in range(3)
                                )
                                zipname_format = (
                                    f"Appify_{username}_{app_name}_{random_string}"
                                )
                                generated_apps_zip = app_storage_path + zipname_format
                                archive_path = shutil.make_archive(
                                    generated_apps_zip, "zip", temp_apps_path
                                )
                                print("Zipped generated apk and aab files")
                        else:
                            print("Error: Unable to change the Appname")
                    else:
                        print("Error : Unable to copy Logo")
                else:
                    print(
                        "Error: Unable to copy Templates to BaseProject in TempDirectory"
                    )

            else:
                print("Error: Unable to copy BaseProject to TempDirectory")

            print("Deleting temp directory......")

        return archive_path
    except Exception as e:
        print("Main Error : ", e)
        print("Something Unexcepted Happened......:-(")
        return None


def copyDirectory(src_path, dest_path):
    try:
        shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        print("File Copied Successfully")
        return True
    except Exception as e:
        print("Error: ", e)
        return False


def editAppName(tmp, app_name):
    string_xml_path = tmp + "/BaseAndroidProject/app/src/main/res/values/strings.xml"
    try:
        tree = ET.parse(string_xml_path)
        root = tree.getroot()

        for string_element in root.findall(".//string"):
            if string_element.get("name") == "app_name":
                string_element.text = app_name

        tree.write(string_xml_path)
        print("App name Edited")
        return True

    except Exception as e:
        print("Error: ", e)
        return False


def changeTemplate(template_src_path, template_dest_path, app_name):
    from cookiecutter.main import cookiecutter

    try:
        cookiecutter(
            template_src_path,
            output_dir=template_dest_path,
            no_input=True,
            extra_context={"app_name": app_name},
        )
        print("Applying App Name")
        return True
    except Exception as e:
        print("Error : ", e)
        return False


def runApkGeneration(tmp):
    from subprocess import Popen, PIPE

    try:
        gradlew_path = tmp + "/BaseAndroidProject"
        os.chdir(gradlew_path)

        command = ["./gradlew", "clean", "--no-daemon", "assemblecustomRelease"]

        process = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        for line in process.stdout:
            print(line, end="")  # Print stdout
        for line in process.stderr:
            print(line, end="")

        process.wait()
        return_code = process.returncode

        if return_code == 0:
            print("Gradle build successful")
            time.sleep(0.5)
            return True
        else:
            print(f"Gradle build failed with return code {return_code}")
            return False

    except Exception as e:
        print("Error:", e)


def runAabGeneration(tmp):
    from subprocess import Popen, PIPE

    try:
        gradlew_path = tmp + "/BaseAndroidProject"
        os.chdir(gradlew_path)

        command = ["./gradlew", "--no-daemon", "bundleRelease"]

        process = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        for line in process.stdout:
            print(line, end="")  # Print stdout
        for line in process.stderr:
            print(line, end="")

        process.wait()
        return_code = process.returncode

        if return_code == 0:
            print("Gradle build successful")
            time.sleep(0.5)
            return True
        else:
            print(f"Gradle build failed with return code {return_code}")
            return False

    except Exception as e:
        print("Error:", e)


def generateApps(
    username=None, template_path=None, app_name=None, client_email=None, app_image=None
):
    if (
        username != None
        and template_path != None
        and app_name != None
        and client_email != None
        and app_image != None
    ):
        print("Process Start....")
        generated_app_archive_path = createTempDir(
            app_name, username, template_path, app_image
        )
        if generated_app_archive_path != None:
            isEmailSent, drive_link = send_email(
                username, app_name, client_email, generated_app_archive_path
            )
            updateArchivePath(
                username,
                app_name,
                app_image,
                drive_link,
                status=isEmailSent,
            )
        else:
            updateArchivePath(username, app_name, app_image, drive_link, status=False)
        print("Process Exit.....")


def updateArchivePath(username, app_name, app_image, drive_link, status=True):
    client = pymongo.MongoClient(
        "mongodb+srv://valli:valli123@appify-test.fauelwk.mongodb.net/appify?retryWrites=true&w=majority&appName=appify-test"
    )

    db = client.appify
    print(db.list_collection_names())
    collection = db.apparchives

    app_image = base64.b64decode(app_image)

    user = collection.find_one({"username": username})

    if user:
        collection.update_one(
            {"_id": user["_id"]},
            {
                "$push": {
                    "archive_path": {
                        "app_name": app_name,
                        "app_image": app_image,
                        "drive_path": drive_link,
                        "status": status,
                    }
                }
            },
        )
        print("Object appended successfully.")
        return True
    else:
        print("User not found.")
        return False


# generateApps(username="Valli", template_path="/home/valli/testing/Templates/Education/template_2",app_name="Valli", client_email="spbharath717@gmail.com")
