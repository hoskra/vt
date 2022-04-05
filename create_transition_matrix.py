import os
from cv2 import INTER_MAX
import numpy as np
import matplotlib.pyplot as plt

def run(input_file = 'out/cartoon_6_0.999_2_0.9'):
  max_to = 0
  min_from = INTER_MAX

  # get frame bouds independently from folder files
  for file in os.listdir(input_file):
    if file.endswith(".txt"):
      from_frame = file.split("_")[0]
      from_frame = int(from_frame.split(".")[0])
      to_frame = file.split("_")[1]
      to_frame = int(to_frame.split(".")[0])
      if to_frame > max_to:
        max_to = to_frame
      if from_frame < min_from:
        min_from = to_frame

  # initialize matrix
  matrix = np.zeros((max_to, max_to))
  transitions = []
  for i in range(max_to):
    transitions.append([])

  # load data for image matrix and transitions file
  for file in os.listdir(input_file):
    if file.endswith(".txt"):
      file = os.path.splitext(file)[0]
      from_frame = file.split("_")[0]
      to_frame = file.split("_")[1]
      path = os.path.join(input_file, file + '.txt')
      tmp = np.loadtxt(path)

      from_frame = int(from_frame)
      to_frame = int(to_frame)

      for row in range(0, tmp.shape[0]):
        for col in range(0, tmp.shape[1]):
          if row == col:
            matrix[from_frame + row][col+from_frame] = 255
          if tmp[row, col] > 0 and col != row + 1:
            matrix[from_frame + row][col+from_frame] = 255
            transitions[row+from_frame].append(col+from_frame)

  # plot matrix
  fig = plt.figure()
  fig.suptitle('Transition matrix')
  plt.xlim(0,len(matrix[0]))
  plt.ylim(0,len(matrix[1]))
  plt.xticks(np.linspace(0, len(matrix[0]), 2))
  plt.yticks(np.linspace(0, len(matrix[1]), 2))
  plt.gca().invert_yaxis()
  plt.imshow(matrix, cmap='viridis')
  plt.savefig(output_name + ".png", bbox_inches='tight')

  # print transitions
  output_name = input_file + "__F:" + str(min_from) +"_T:" + str(max_to)
  f = open(output_name + ".txt", "w")
  for i, t in enumerate(transitions):
    t = list(set(t))
    transitions[i] = t
    f.write(str(t) + "\n")