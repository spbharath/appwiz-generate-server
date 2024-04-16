# importing the module
import shutil
import os
import time
import random
import string
from tempfile import TemporaryDirectory
import xml.etree.ElementTree as ET
from customemailgen import send_email

def createTempDir(app_name, username, template_path):

    try:

        with TemporaryDirectory(dir = "E:/ReactNative/AppifyProject") as tmp:
            
            print("Created", tmp)
            base_src_path = "E:/ReactNative/AppifyProject/Project"
            
            if copyDirectory(base_src_path, tmp):

                print("Copied BaseProject to TempDirectory")
                template_src_path = template_path   # "E:/ReactNative/AppifyProject/Templates/Education/template_1"
                template_dest_path = tmp + "/BaseAndroidProject/app/src/main/assets/"
                
                if changeTemplate(template_src_path, template_dest_path, app_name):
                    print("Copied Templates to BaseProject in TempDirectory")
                    if editAppName(tmp, app_name):
                        print("Changed Appname to " + app_name)
                        print("Generating APK...........")          
                        app_storage_path = "E:/ReactNative/AppifyProject/apps/"
                        app_name_format = f"Appify_{username}_{app_name}"
                        temp_apps_path = tmp + "/appify_apps/"
                        apk = False; 
                        aab = False
                        if runApkGeneration(tmp):
                            generated_app_path = tmp + "/BaseAndroidProject/app/build/outputs/apk/customRelease/app-customRelease.apk"
                            apk_path = temp_apps_path + app_name_format + ".apk"
                            shutil.move(generated_app_path, apk_path)
                            os.chdir("E:/ReactNative/AppifyProject")
                            print("Generated APK copied to the apps bin")
                            apk = True
                        else:
                            print("Error : Apk Generation Failed!")
                        if runAabGeneration(tmp):
                            generated_app_path = tmp + "/BaseAndroidProject/app/build/outputs/bundle/release/app-release.aab"
                            aab_path = temp_apps_path + app_name_format + ".aab"
                            shutil.move(generated_app_path, aab_path)
                            os.chdir("E:/ReactNative/AppifyProject")
                            print("Generated AAB copied to the apps bin")
                            aab = True
                        else:
                            print("Error : AAB Generation Failed!")  
                        if(apk and aab):
                            random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))
                            zipname_format = f"Appify_{username}_{app_name}_{random_string}"
                            generated_apps_zip = app_storage_path + zipname_format
                            archive_path = shutil.make_archive(generated_apps_zip,'zip', temp_apps_path)
                            print("Zipped generated apk and aab files")
                    else:
                        print("Error: Unable to change the Appname")
                else:
                    print("Error: Unable to copy Templates to BaseProject in TempDirectory")

            else:
                print("Error: Unable to copy BaseProject to TempDirectory")
            
            print("Deleting temp directory......")

        return archive_path
    except Exception as e:
        print("Main Error : ", e)
        print("Something Unexcepted Happened......:-(")
        # return False


def copyDirectory(src_path, dest_path):
    try:
        shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        print("File Copied Successfully")
        return True
    except Exception as e:
        print("Error: ",e)
        return False    
    


def editAppName(tmp, app_name):
    string_xml_path  = tmp + "/BaseAndroidProject/app/src/main/res/values/strings.xml"
    try:
        tree = ET.parse(string_xml_path)
        root = tree.getroot()

        for string_element in root.findall('.//string'):
            if string_element.get('name') == 'app_name':
                string_element.text = app_name

        tree.write(string_xml_path)
        print("App name Edited")
        return True
    
    except Exception as e:
        print("Error: ",e)
        return False

    


def changeTemplate(template_src_path, template_dest_path, app_name):
    from cookiecutter.main import cookiecutter
    try:
        cookiecutter(
        template_src_path,
        output_dir=template_dest_path,
        no_input=True,
        extra_context={
            "app_name": app_name
        }
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
        
        process =  Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
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

        command = ["gradlew.bat", "--no-daemon", "bundleRelease"]
        
        process =  Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
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

def generateApps(username = None, template_path = None, app_name = None, client_email = None):
    if (username != None and template_path !=None and app_name != None and client_email != None):
        print("Process Start....")
        generated_app_archive_path = createTempDir(app_name, username, template_path)
        send_email(username, app_name, client_email, generated_app_archive_path)
        print("Process Exit.....")
    