import os
import multiprocessing

import frames_analysis
import utils
import config

clock_parameters = {
  "input_folder"    : "clock",
  "qualityExponent" : 2,
  "futureCostAlpha" : 0.999,
  "sigmaMult"       : 2,
  "thresholdValue"  : 0.5,
}

cartoon_parameters = {
  "input_folder"    : "cartoon",
  "qualityExponent" : 3,
  "futureCostAlpha" : 0.999,
  "sigmaMult"       : 2,
  "thresholdValue"  : 0.6,
}

grass_parameters = {
  "input_folder"    : "grass",
  "qualityExponent" : 7,
  "futureCostAlpha" : 0.999,
  "sigmaMult"       : 2,
  "thresholdValue"  : 0.6,
}

stairs1_parameters = {
  "input_folder"    : "stairs1",
  "qualityExponent" : 5,
  "futureCostAlpha" : 0.999,
  "sigmaMult"       : 2,
  "thresholdValue"  : 0.7,
}

stairs2_parameters = {
  "input_folder"    : "stairs2",
  "qualityExponent" : 7,
  "futureCostAlpha" : 0.999,
  "sigmaMult"       : 2,
  "thresholdValue"  : 0.6,
}

parameters = config.parameters;

MULTIPROCESSING = True

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

    print("")
    print("Creating transition matrix ...")
    output_name = utils.create_transition_matrix(out_path)
    print("\tMatrix output located at out/"+ output_name+".png")
    print("\tCheck "+ output_name+"/*.png files and adjust parameters accordingly!")
    print("Generate config.js file ...")
    output_name = utils.create_config_file(parameters["input_folder"], output_name)
    print("\tDone!")
    print("\tTo run video-texture player, please type `python3 -m http.server`")
    print("\tand visit localhost:8000 in your browser.")
