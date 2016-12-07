import numpy as np
import cv2
shape = (1, 10, 2)  # Needs to be a 3D array

# source = np.random.randint(0, 100, shape).astype(np.int)
source = np.float32([[306, 184],[88, 188],[270, 206],[56, 215],[93, 215]]).reshape(-1,1,2)
print(source)

# target = source + np.array([1, 0]).astype(np.int)
target = np.float32([[1317, 181],[1100, 192],[1276, 205],[1072, 218],[1104, 217]]).reshape(-1,1,2)
print(target)

transformation = cv2.estimateRigidTransform(source, target, False)
print(transformation)
t = np.zeros((5,1))

cv2.warpAffine(source, t, transformation, [5,1])

# (306, 184) (1317, 181)
# (306, 184) (1317, 181)
# (88, 188) (1100, 192)
# (270, 206) (1276, 205)
# (56, 215) (1072, 218)
# (93, 215) (1104, 217)