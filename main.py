import os
import multiprocessing

import frames_analysis
import create_transition_matrix

clock_parameters = {
  "input_folder"    : "clock",
  "qualityExponent" : 2,
  "futureCostAlpha" : 0.999,
  "sigmaMult"       : 2,
  "thresholdValue"  : 0.5,
}
skeleton_dance_parameters = {
  "input_folder"    : "skeleton_dance",
  "qualityExponent" : 6,
  "futureCostAlpha" : 0.999,
  "sigmaMult"       : 2,
  "thresholdValue"  : 0.6,
}
cartoon_dance_parameters = {
  "input_folder"    : "cartoon",
  "qualityExponent" : 3,
  "futureCostAlpha" : 0.999,
  "sigmaMult"       : 2,
  "thresholdValue"  : 0.6,
}

MULTIPROCESSING = True
parameters = cartoon_dance_parameters

step = 100
half = int(step/2)
parameters_string = '_'.join([str(parameters[i]) for i in parameters])
out_path = os.path.join('out', parameters_string)

def run(arg):
  from_frame  = arg[0]
  to_frame    = arg[1]
  frames_analysis.videotexture_analysis(parameters, out_path, from_frame, to_frame)

if __name__ == '__main__':
    if not os.path.exists(out_path):
      os.makedirs(out_path)

    frames_cnt = len(os.listdir(parameters["input_folder"]))
    if MULTIPROCESSING:
      pool = multiprocessing.Pool()
      inputs = []
      processed_frames = 0
      for i in range(0, frames_cnt, half):
        from_frame = i
        to_frame = i + step
        if(to_frame > frames_cnt):
          to_frame = frames_cnt
        inputs.append([from_frame, to_frame])
        if processed_frames == frames_cnt:
          break

      # todo: limit processes
      pool = multiprocessing.Pool(processes=len(inputs))
      pool.map(run, inputs)
      pool.close()
    else:
      run([0, frames_cnt])

    print("Creating transition matrix")
    create_transition_matrix.run(out_path)
