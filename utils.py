import os
from cv2 import INTER_MAX
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import json
import platform

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '█', printEnd = "\r"):
    # https://www.programcreek.com/python/?CodeExample=print+progress+bar
    """
    Call in a loop to create terminal progress bar
    @params:
    iteration   - Required  : current iteration (Int)
    total       - Required  : total iterations (Int)
    prefix      - Optional  : prefix string (Str)
    suffix      - Optional  : suffix string (Str)
    decimals    - Optional  : positive number of decimals in percent complete (Int)
    length      - Optional  : character length of bar (Int)
    fill        - Optional  : bar fill character (Str)
    printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)

    if iteration == total:
        print()

def create_config_file(input_file, output_name) :
  cnt = len(os.listdir(input_file))
  fromFrame = sorted(os.listdir(input_file))[0]
  [fromFrame, extension]  = fromFrame.split(".")
  fromFrame = int(fromFrame)
  toFrame = fromFrame + cnt - 1

  config = {
    "filename": output_name,
    "folder": input_file,
    "extension": extension,
    "from": fromFrame,
    "to": toFrame,
    "slice": False
  }

  with open('src/config.js', 'w') as outfile:
    outfile.write("const config = ")
    json.dump(config, outfile)
    outfile.write(";")

  system = platform.system()
  divider = "/"
  if system == "Windows":
    divider = "\\"

  with open('src/saved_configs.js', 'a') as outfile:
    outfile.write("const ")
    name = output_name.split(divider)[1].replace(".","_").replace(":","_")
    outfile.write(name)
    outfile.write(" = ")
    json.dump(config, outfile)
    outfile.write(";\n")

def create_transition_matrix(input_file):
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
  matplotlib.use('agg')   ## https://stackoverflow.com/a/28904054
  fig = plt.figure()
  fig.suptitle('Transition matrix')
  plt.xlim(0,len(matrix[0]))
  plt.ylim(0,len(matrix[1]))
  plt.xticks(np.linspace(0, len(matrix[0]), 2))
  plt.yticks(np.linspace(0, len(matrix[1]), 2))
  plt.gca().invert_yaxis()
  plt.imshow(matrix, cmap='viridis')
  plt.savefig(input_file + ".png", bbox_inches='tight')

  # print transitions
  f = open(input_file + ".txt", "w")
  for i, t in enumerate(transitions):
    t = list(set(t))
    transitions[i] = t
    f.write(str(t) + "\n")

  return input_file