# importing the module
import shutil
import os
import time
import random
import string
from tempfile import TemporaryDirectory
import xml.etree.ElementTree as ET
from customemailgen import send_email
import pymongo
import base64
from save_logo import save_logo_from_base64


def createTempDir(app_name, username, template_path):

    try:

        with TemporaryDirectory(
            dir="D:/Expo-Projects/Valli-Python-test/AppifyProject"
        ) as tmp:

            print("Created", tmp)
            base_src_path = (
                "D:/Expo-Projects/Valli-Python-test/AppifyProject/Project/Test"
            )

            if copyDirectory(base_src_path, tmp):
                print("Copied BaseProject to TempDirectory")
                template_src_path = template_path  # "D:/Expo-Projects/Valli-Python-test/AppifyProject/Templates/Education/template_1"
                template_dest_path = tmp + "/BaseAndroidProject/app/src/main/assets/"

                if changeTemplate(template_src_path, template_dest_path, app_name):
                    print("Copied Templates to BaseProject in TempDirectory")
                    logo_prjt_path = tmp + "/BaseAndroidProject"
                    if save_logo_from_base64(logo_prjt_path):
                        if editAppName(tmp, app_name):
                            print("Changed Appname to " + app_name)
                            print("Generating APK...........")
                            app_storage_path = (
                                "D:/Expo-Projects/Valli-Python-test/AppifyProject/apps/"
                            )
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
                                os.chdir(
                                    "D:/Expo-Projects/Valli-Python-test/AppifyProject"
                                )
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
                                os.chdir(
                                    "D:/Expo-Projects/Valli-Python-test/AppifyProject"
                                )
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

        command = ["gradlew.bat", "clean", "--no-daemon", "assemblecustomRelease"]

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
            os.chdir(tmp)
            process.terminate()
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

        command = ["gradlew.bat", "--no-daemon", "bundleRelease"]

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
        generated_app_archive_path = createTempDir(app_name, username, template_path)
        if generated_app_archive_path != None:
            isEmailSent, drive_link = send_email(
                username, app_name, client_email, generated_app_archive_path
            )
            # updateArchivePath(
            #     username,
            #     app_name,
            #     app_image,
            #     drive_link,
            #     status=isEmailSent,
            # )
            print("Generation Passed")
        else:
            # updateArchivePath(username, app_name, app_image, drive_link, status=False)
            print("Generation Failed")
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


base64_string = "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"

generateApps(
    username="Valli",
    template_path="D:/Expo-Projects/Valli-Python-test/AppifyProject/Templates/Education/template_1",
    app_name="Valli",
    client_email="spbharath717@gmail.com",
    app_image=base64_string,
)
