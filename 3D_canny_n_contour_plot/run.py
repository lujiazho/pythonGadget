import nibabel                  # read nii
import numpy as np
import SimpleITK as sitk        # 3d canny
import matplotlib.pyplot as plt

# 3d canny for nii
data_dir = r'sub-05_T1w.nii'
data_nii = sitk.ReadImage(data_dir)
origin = data_nii.GetOrigin()
spacing = data_nii.GetSpacing()
direction = data_nii.GetDirection()

# change data type before edge detection
data_float_nii = sitk.Cast(data_nii, sitk.sitkFloat32)

canny_op = sitk.CannyEdgeDetectionImageFilter()
canny_op.SetLowerThreshold(100)
canny_op.SetUpperThreshold(200)
canny_op.SetVariance(1)
canny_op.SetMaximumError(0.5)
canny_sitk = canny_op.Execute(data_float_nii)
canny_sitk = sitk.Cast(canny_sitk, sitk.sitkInt16)

canny_sitk.SetOrigin(origin)
canny_sitk.SetSpacing(spacing)
canny_sitk.SetDirection(direction)
sitk.WriteImage(canny_sitk, './canny_edge.nii')

# 3d visualization
img = nibabel.load("./canny_edge.nii").get_data()
print(img.min(), img.max())
fig = plt.figure()
 
# syntax for 3-D projection
ax = plt.axes(projection ='3d')

resolution = 6
s = set()
# up and down
for i in range(0, img.shape[0], resolution):
    for j in range(0, img.shape[1], resolution):
        flag_k1 = 0
        flag_k2 = 0
        for k1, k2 in zip(range(img.shape[2]-1, -1, -2), range(0, img.shape[2], 2)):
            if not flag_k1 and img[i][j][k1] > 0:
                s.add((i,j,k1))
                flag_k1 = 1
            if not flag_k2 and img[i][j][k2] > 0:
                s.add((i,j,k2))
                flag_k2 = 1
            if flag_k1 and flag_k2:
                break
num1 = len(s)
# left and right
for k in range(0, img.shape[2], resolution):
    for j in range(0, img.shape[1], resolution):
        flag_i1 = 0
        flag_i2 = 0
        for i1, i2 in zip(range(img.shape[0]-1, -1, -2), range(0, img.shape[0], 2)):
            if not flag_i1 and img[i1][j][k] > 0:
                s.add((i1,j,k))
                flag_i1 = 1
            if not flag_i2 and img[i2][j][k] > 0:
                s.add((i2,j,k))
                flag_i2 = 1
            if flag_i1 and flag_i2:
                break
num2 = len(s) - num1
# front and back
for k in range(0, img.shape[2], resolution):
    for i in range(0, img.shape[0], resolution):
        flag_j1 = 0
        flag_j2 = 0
        for j1, j2 in zip(range(img.shape[1]-1, -1, -2), range(0, img.shape[1], 2)):
            if not flag_j1 and img[i][j1][k] > 0:
                s.add((i,j1,k))
                flag_j1 = 1
            if not flag_j2 and img[i][j2][k] > 0:
                s.add((i,j2,k))
                flag_j2 = 1
            if flag_j1 and flag_j2:
                break
num3 = len(s) - num1 - num2

s = np.array(list(s))
x = s[:,0]
y = s[:,1]
z = s[:,2]
c = x+y
print(x.shape)
ax.scatter(x, y, z, c=c, s=6)

# syntax for plotting
ax.set_title('3d Scatter plot sMRI')
plt.axis('off')
plt.show()