import numpy as np
import cv2 as cv2
import os
import matplotlib.pyplot as plt
import math
import scipy.signal
import copy

import utils

input_folder = "input"
images_folder = "images_folder"
img_list = []

''' Read frames from input folder and save grayscaled pixel value '''
for filename in os.listdir(input_folder):
  value = cv2.imread(os.path.join(input_folder, filename), cv2.IMREAD_GRAYSCALE)
  img_list.append(value)

''' Prepare empty matrix '''
img_list = np.array(img_list)
frames_count = len(img_list)
matrix = np.zeros((frames_count, frames_count), dtype='float')

''' Get visual difference '''
def get_distance(a, b):
    return np.sum( (a - b) ** 2 )       #
    return np.linalg.norm(a - b, 'fro') # frobenius norm
    return np.linalg.norm(a - b)        # Euclidean norm

for i in range(frames_count):
  for j in range(frames_count):
    matrix[i,j] = get_distance(img_list[i], img_list[j])
    utils.printProgressBar(i*frames_count+j+1, frames_count*frames_count, prefix = 'Calculating distances:\t', suffix = 'Complete')

imgplot = plt.imshow(matrix)
plt.savefig(images_folder + '/distances.png')

''' Preserve dynamics '''
kernel = np.diag(np.array([ 0.0625,  0.25  ,  0.375 ,  0.25  ,  0.0625], dtype=float))
diff2 = []

for i in range(frames_count):
  for j in range(frames_count):
    diff2 = scipy.signal.convolve2d(matrix, kernel, mode='valid')
    utils.printProgressBar(i*frames_count+j+1, frames_count*frames_count, prefix = 'Preserve dynamics:\t', suffix = 'Complete')

imgplot = plt.imshow(diff2)
plt.savefig(images_folder + '/dynamics.png')

''' Future costs '''
qualityExponent = 3
futureCostAlpha = 0.999

tmp = np.zeros((diff2.shape[0], diff2.shape[1]))
diff3 = np.zeros((diff2.shape[0], diff2.shape[1]))

# Initialise with D''ij = (D'ij)^p
for i in range(1, diff2.shape[0]):
  for j in range(0, diff2.shape[1]):
    tmp[i][j] = math.pow(diff2[i - 1][j], qualityExponent)

# Continue until an iteration does not change the matrix
while True:
  utils.printProgressBar(0, 1, prefix = 'Future costs:\t', suffix = 'Complete')
  for i in range(diff2.shape[0] - 1, 0, -1):
    for j in range(0, diff2.shape[1] - 1):

      # Determine the (D'_ij)^p term
      future_cost_base = math.pow(diff2[i][j], qualityExponent)

      # Determine the row minimum m_j = min_k D''_jk
      k_min = tmp[j].min()

      future_cost_summation = futureCostAlpha * k_min
      tmp[i][j] = future_cost_base + future_cost_summation

  if (tmp == diff3).all():
    utils.printProgressBar(1, 1, prefix = 'Future costs:  \t\t', suffix = 'Complete')
    break
  else:
    diff3 = tmp


imgplot = plt.imshow(diff3)
plt.savefig(images_folder + '/cost.png')

''' Probability '''
sigmaMult = 2
sigma = float(diff3.mean()) * sigmaMult
diff4 = np.zeros((diff3.shape[0] - 1, diff3.shape[1] - 1))

# Determine each of the probabilities
for x in range(0, diff3.shape[0] - 1):
  for y in range(0, diff3.shape[1] - 1):
    diff4[x][y] = math.exp((-diff3[x + 1][y]) / sigma)

imgplot = plt.imshow(diff4)
plt.savefig(images_folder + '/probabilities.png')


''' Prune '''
thresholdValue = 0.6 # Lower will allow more transitions

def determine_local_maxima(matrix):
  thresholded_matrix = matrix
  (height, width) = matrix.shape

  for i in range(0, height):
    maxima = scipy.signal.argrelextrema(matrix[i], np.greater)[0]
    for j in range(0, width):
      if j not in maxima:
        matrix[i][j] = 0
      utils.printProgressBar(i*height+j+1, height*width, prefix = 'Local maximum:\t\t', suffix = 'Complete')
  return thresholded_matrix

def threshold_matrix(matrix, threshold):
  thresholded_matrix = matrix
  low_value_indices = thresholded_matrix < threshold
  thresholded_matrix[low_value_indices] = 0
  return thresholded_matrix

''' Determine Local Maxima '''
future_matrix = determine_local_maxima(diff4)
imgplot = plt.imshow(future_matrix)
plt.savefig(images_folder + '/local_maxima.png')

''' Threshold '''
future_matrix = threshold_matrix(copy.copy(future_matrix), thresholdValue)
imgplot = plt.imshow(future_matrix)
plt.savefig(images_folder + '/threshold.png')

print()
