import os, shutil, plistlib, time, sys

line = "--------------------------------------------------"

def noline(string):
    print(string,end="")

def title(string):
    print(line)
    print("{:^50}".format(string))
    print(line)

def isfile(string):
    return os.path.isfile(string)

def clear():
    os.system("clear")

neededfiles = [r"../AppleDiagnostics.chunklist", r"../AppleDiagnostics.dmg", r"../BaseSystem.chunklist", r"../BaseSystem.dmg", r"../InstallESDDmg.pkg", r"../InstallInfo.plist"]

def copyfiles(sharedsupportloc):
    for f in neededfiles:
        noline("Copying {}... ".format(f))
        shutil.copy(f, sharedsupportloc)
        print("Done.")

def editplist():
    fp = open(r"./InstallInfo.plist","rb")
    installinfo = plistlib.load(fp)
    del installinfo["Payload Image Info"]["chunklistURL"]
    del installinfo["Payload Image Info"]["chunklistid"]
    installinfo["Payload Image Info"]["URL"] = "InstallESD.dmg"
    installinfo["Payload Image Info"]["id"] = "com.apple.dmg.InstallESD"
    plistlib.dump(installinfo, open(r"./InstallInfo.plist", "wb"))

def packapp():

    clear()
    title("Choose macOS Version")
    print("1: High Sierra")
    print("2: Mojave")
    print("Q: Quit")
    print("M: Main Menu")
    option = input("Please enter an option: ")
    version = ""
    if option == "1":
        version = "High Sierra"
    elif option == "2":
        version = "Mojave"
    elif option == "Q":
        quit()
    elif option == "M":
        mainmenu()
    else:
        packapp()

    clear()
    sharedsupportloc = r"./Install macOS {}.app/Contents/SharedSupport".format(version)

    title("Packing Files to Application")

    noline("Mounting BaseSystem.dmg... ")
    os.system("hdiutil attach ../BaseSystem.dmg")
    print("Done.")

    noline("Copying Installer from BaseSystem.dmg... ")
    os.system("cp -rf /Volumes/'macOS Base System'/'Install macOS {}.app' ./'Install macOS {}.app'".format(version, version))
    print("Done.")

    noline("Making Directories... ")
    os.makedirs(sharedsupportloc)
    print("Done.")

    print("Copying Files...")
    copyfiles(sharedsupportloc)
    print("Done.")

    noline("Editting InstallInfo.plist... ")
    os.chdir(sharedsupportloc)
    editplist()
    print("Done.")

    noline("Renaming InstallESD.dmg... ")
    os.rename("InstallESDDmg.pkg", "InstallESD.dmg")
    print("Done.")

    noline("Deleting Files")
    os.chdir(r"../Frameworks/OSInstallerSetup.framework")
    os.remove("OSInstallerSetup")
    shutil.rmtree("Resources")
    os.remove("Versions/Current")
    print("Done")

    noline("Creating Alias")
    os.chdir("Versions")
    os.system("ln -s A")
    os.rename("A","Current")
    os.chdir("../")
    os.system("ln -s Versions/A/OSInstallerSetup")
    os.system("ln -s Versions/A/Resources")
    print("Done.")

    print("All Done")
    time.sleep(1)

    mainmenu()
    

def convert():
    pass

def checkfiles():
    clear()
    title("Checking Required Files...")
    time.sleep(0.5)
    for f in neededfiles:
        if isfile(f) == False:
            print("Missing Files.")
            sys.exit()

def quit():
    print("Goodbye! Have a good day!")
    sys.exit()

def mainmenu():
    clear()
    title("Main Menu")
    print("1: Pack files to an Install macOS Application")
    print("2: Convert Network Recovery macOS Installer USB to a Full Installer")
    print("Q: Quit")
    option = input("Enter an option: ")
    if option == "Q" or option == "q":
        quit()
    elif option == "1":
        packapp()
    elif option == "2":
        convert()
    else:
        mainmenu()

def main():
    checkfiles()
    mainmenu()

if __name__ == "__main__":
    main()