# OpenCVSimpleCameraCalibration

There are way too many complex systems to get your camera's parameters. I wanted something simple that just worked.

1) Print pattern.jpg and stick it onto something straight
2) Run CameraCalibrator.py - and move your camera around the printed pattern (or move the printed pattern around if your camera is stationary).
 2a) You can change the amount of pictures necessary to calibrate by changing the "pointsToCollect" variable.
3) Once 100% is reached, it will generate a CameraCalibration file, which you can read with python pickle.

The available properties are:
ret, mtx, dist, rvecs, tvecs, cameraMatrix, roi, totalError, meanError