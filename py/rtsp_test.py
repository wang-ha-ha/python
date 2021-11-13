import cv2 

url = "rtsp://admin:kk54881626@192.168.2.2/Streaming/Channels/101"

vcap = cv2.VideoCapture(url)

while(1):

    ret, frame = vcap.read()
    cv2.imshow('VIDEO', frame)
    cv2.waitKey(1)