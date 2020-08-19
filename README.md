## Note:
**This was a school project where our team used a Raspberry Pi with a camera to recognize students to be able to log their attendance in class.
This is a proof-of-concept code and is only meant to be used for feature presentation.**

The server side was created because the OpenCV on Raspberry Pi was too slow to learn faces.
Therefore, the learning code was moved to a VPS and become automated.
The client side code that runs on the Raspberry Pi can be found [here](https://github.com/kivulallo/attendance-app-client-public).


## How it works:
* This code needs to be running first.
* A given source - which can be a website, smartphone app, etc. - uploads images to the PHP endpoint by sending a multipart POST request.
* The server listens to modifications on the given directory. If an image was uploaded, it will start the training process.
* Once the training is done, it sends a notification message to the MQTT channel the clients (RPis) are subscribed to.
* The RPi clients will download the updated training file with the new face information and reload themselves.

## How to run:

```$ python3 imagesWatcher.py [folderToWatch]```<br>
Default folderToWatch: ```./images```

