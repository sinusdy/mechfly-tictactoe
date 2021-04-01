# import required libraries
from vidgear.gears import NetGear
from vidgear.gears import PiGear
import cv2
import sys

# open pi video stream
stream = PiGear(
    resolution=(640,480),
    # colorspace="COLOR_BGR2HSV"
).start()

# define various tweak flags
options = {"flag": 0, "copy": False, "track": False}

# Define Netgear Server with default parameters
server = NetGear(
    address=sys.argv[1],
    port=sys.argv[2],
    protocol="tcp",
    pattern=1,
    logging=True,
    receive_mode=True,
    **options
)

# loop over until KeyBoard Interrupted
while True:

    try:

        # read frames from stream
        frame = stream.read()

        # check for frame if Nonetype
        if frame is None:
            break

        # {do something with the frame here}

        # send frame to server
        server.send(frame)

    except KeyboardInterrupt:
        break

# safely close video stream
stream.stop()

# safely close server
server.close()