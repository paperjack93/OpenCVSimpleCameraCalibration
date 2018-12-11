import pickle;

try: fileObject = open("cameraCalibration",'rb'); 
except: fileObject = None;

try: data = pickle.load(fileObject);
except: data = None;

if(fileObject != None): fileObject.close();
if(data != None): print(format(data));
