import numpy as np
import cv2
import pickle

pointsToCollect = 50;

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001);
objp = np.zeros((9*6,3), np.float32);
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2);
objpoints = []; # 3d point in real world space
imgpoints = []; # 2d points in image plane.

camera = cv2.VideoCapture(0);
ret, img = camera.read();
gray = None;
while True:
    ret, img = camera.read();
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
    ret, corners = cv2.findChessboardCorners(gray, (9,6), None);
    if ret == True:
        objpoints.append(objp);
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria);
        imgpoints.append(corners);
        cv2.drawChessboardCorners(img, (9,6), corners2, ret);
    percent = len(objpoints)/pointsToCollect * 100;
    if(percent >= 100): break;
    cv2.putText(img, format(percent)+'%', (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2);
    cv2.imshow('img', img);
    if(ret == True): cv2.waitKey(100);
    else: cv2.waitKey(1);

cv2.destroyAllWindows();
    
h, w = img.shape[:2];

print("Data collected, starting calibration...");
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (w,h), None, None);
    
cameraMatrix, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

totalError = 0;
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist);
    error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2);
    totalError += error;

meanError = totalError/len(objpoints);
print("total error: " + format(totalError) + " meanError: " + format(meanError));

data = {
    "ret": ret,
    "mtx": mtx,
    "dist": dist,
    "rotationVectors": rvecs,
    "translationVectors": tvecs,
    "cameraMatrix": cameraMatrix,
    "roi":roi,
    "totalError":totalError,
    "meanError":meanError
}

print(format(data));
fileObject = open("cameraCalibration",'wb'); 
pickle.dump(data,fileObject);
fileObject.close()

while True:
    ret, img = camera.read();
    img = cv2.undistort(img, mtx, dist, None, cameraMatrix);
    cv2.putText(img, "total error: " + format(totalError) + " meanError" + format(meanError), (30,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2);
    cv2.imshow('img', img);
    cv2.waitKey(1);
