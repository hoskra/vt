
import numpy as np
import cv2 as cv2
import os
import matplotlib.pyplot as plt
import math
import scipy.signal
import copy
import utils

def videotexture_analysis(parameters, out_path, from_frame = -1, to_frame = -1):
  ''' Read frames from input folder and save grayscaled pixel value '''
  img_list = []
  fig, ax = plt.subplots(2, 3)

  qualityExponent = parameters["qualityExponent"]
  futureCostAlpha = parameters["futureCostAlpha"]
  sigmaMult       = parameters["sigmaMult"]
  thresholdValue  = parameters["thresholdValue"]
  input_folder    = parameters["input_folder"]

  input_frames = sorted(os.listdir(input_folder))

  for i in range(from_frame, to_frame):
    filename = input_frames[i]
    value = cv2.imread(os.path.join(input_folder, filename), cv2.IMREAD_GRAYSCALE)
    img_list.append(value)

  ''' Prepare empty matrix '''
  img_list = np.array(img_list)
  frames_count = len(img_list)
  diff1 = np.zeros((frames_count, frames_count), dtype='float')

  ''' Get visual difference '''
  def get_distance(a, b):
      return np.sum( (a - b) ** 2 )       #
      return np.linalg.norm(a - b, 'fro') # frobenius norm
      return np.linalg.norm(a - b)        # Euclidean norm

  for i in range(frames_count):
    for j in range(frames_count):
      diff1[i,j] = get_distance(img_list[i], img_list[j])
      utils.printProgressBar(i*frames_count+j+1, frames_count*frames_count, prefix = 'Calculating distances:\t', suffix = 'Complete')

  ax[0, 0].imshow(diff1)
  ax[0, 0].set_title("distances")

  ''' Preserve dynamics '''
  kernel = np.diag(np.array([ 0.0625,  0.25  ,  0.375 ,  0.25  ,  0.0625], dtype=float))
  diff2 = []

  for i in range(frames_count):
    for j in range(frames_count):
      diff2 = scipy.signal.convolve2d(diff1, kernel, mode='valid')
      utils.printProgressBar(i*frames_count+j+1, frames_count*frames_count, prefix = 'Preserve dynamics:\t', suffix = 'Complete')

  ax[0, 1].set_title("dynamics")
  ax[0, 1].imshow(diff2)

  ''' Future costs '''
  tmp = np.zeros((diff2.shape[0], diff2.shape[1]))
  diff3 = np.zeros((diff2.shape[0], diff2.shape[1]))

  if futureCostAlpha <= 0:
    diff3 = diff2
  else:
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

  ax[0, 2].set_title("future_cost")
  ax[0, 2].imshow(diff3)

  ''' Probability '''
  sigma = float(diff3.mean()) * sigmaMult
  diff4 = np.zeros((diff3.shape[0] - 1, diff3.shape[1] - 1))

  # Determine each of the probabilities
  for x in range(0, diff3.shape[0] - 1):
    for y in range(0, diff3.shape[1] - 1):
      diff4[x][y] = math.exp((-diff3[x + 1][y]) / sigma)

  ax[1, 0].set_title("probabilities")
  ax[1, 0].imshow(diff4)

  ''' Prune '''
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
  future_matrix1 = determine_local_maxima(diff4)
  ax[1, 1].set_title("local_maxima")
  ax[1, 1].imshow(future_matrix1)

  ''' Threshold '''
  future_matrix2 = threshold_matrix(copy.copy(future_matrix1), thresholdValue)
  ax[1, 2].set_title("threshold")
  ax[1, 2].imshow(future_matrix2)

  def graphAxes(row, column, matrix):
    plt.sca(ax[row, column])
    plt.xlim(0,len(matrix[0]))
    plt.ylim(0,len(matrix[1]))
    plt.xticks(np.linspace(0, len(matrix[0]), 2))
    plt.yticks(np.linspace(0, len(matrix[1]), 2))
    plt.gca().invert_yaxis()

  graphAxes(0, 0, diff1)
  graphAxes(0, 1, diff2)
  graphAxes(0, 2, diff3)
  graphAxes(1, 0, diff4)
  graphAxes(1, 1, future_matrix1)
  graphAxes(1, 2, future_matrix2)

  fig.suptitle("Q: " + str(qualityExponent) + " alpha: \
    " + str(futureCostAlpha) + " sigma: \
      " + str(sigmaMult) + " t: " + str(thresholdValue))

  name = str(from_frame) + '_' + str(to_frame)
  name = os.path.join(out_path, name)
  plt.savefig(name, bbox_inches='tight')
  np.savetxt(name + ".txt", future_matrix2)
