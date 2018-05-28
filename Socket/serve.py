import socket
import os
import sys
import struct
import cv2

cap = cv2.VideoCapture(0)
index = 0
#开启摄像头
while True:
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('p'):
        cv2.imwrite("kk.jpg", frame)
        index = index + 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 6666))
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print(s.recv(1024))

    while 1:
        filepath = b'D:\ProgramingFile\Python\Socket\kk.jpg '# raw_input('please input file path: ')
        if os.path.isfile(filepath):

            fileinfo_size = struct.calcsize('128sl')

            fhead = struct.pack('128sl', os.path.basename(filepath),
                                os.stat(filepath).st_size)
            s.send(fhead)
            print("client filepath: {0}".format(filepath))
            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print("{0} file send over...".format(filepath))
                    break
                s.send(data)
        s.close()
        break


if __name__ == '__main__':
    socket_client()