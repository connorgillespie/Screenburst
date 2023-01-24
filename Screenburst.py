#    _____                           __                    __
#   / ___/_____________  ___  ____  / /_  __  ____________/ /_
#   \__ \/ ___/ ___/ _ \/ _ \/ __ \/ __ \/ / / / ___/ ___/ __/
#  ___/ / /__/ /  /  __/  __/ / / / /_/ / /_/ / /  (__  ) /_
# /____/\___/_/   \___/\___/_/ /_/_.___/\__,_/_/  /____/\__/
#
# Author: Connor Gillespie

import datetime
import os.path
import time as sleep
import zipfile
from PIL import ImageGrab

# Check for output directory.
images = os.path.join(os.getcwd(), "Images")
if not os.path.exists(images):
    os.mkdir(images)
    print("Generated output folder at %s." % images)

# Create temporary folder.
time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
temporary = os.path.join(images, time)
os.mkdir(temporary)

try:
    # Take a screenshot every five seconds.
    counter = 1
    while 1:
        image = ImageGrab.grab()
        image.save(os.path.join(temporary, str(counter) + ".png"))
        print("Screenshot %s.png saved." % counter)
        counter += 1
        sleep.sleep(5)

except KeyboardInterrupt:
    # Zip files.
    with zipfile.ZipFile(os.path.join(images, time + ".zip"), "w") as zip:
        for root, dirs, files in os.walk(temporary):
            for file in files:
                zip.write(os.path.join(root, file),
                          os.path.relpath(os.path.join(root, file), os.path.join(temporary, '..')))

    # Delete files inside temporary folder.
    for root, dirs, files in os.walk(temporary):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))

    # Delete temporary folder.
    os.rmdir(temporary)

    # Print output information.
    print("Screenshots have been zipped to %s." % os.path.join(images, time + ".zip"))
