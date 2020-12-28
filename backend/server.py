import tensorflow as tf

import numpy as np
import os
import pickle
from model import BahdanauAttention, CNN_Encoder, RNN_Decoder
import argparse

from extract_frames import extract_frames
from cluster_frames import cluster_frames
from drop_frames import drop_frames

from utils import evaluate_beam_search, evaluate_brute_force

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    # Currently, memory growth needs to be the same across GPUs
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Memory growth must be set before GPUs have been initialized
    print(e)

def get_captions(path):
  results = {}
  x = [x[0] for x in os.walk(path)]
  for dir in x[1:]:
      files = os.listdir(dir)
      for file in files:
        result, _ = evaluate_beam_search(dir + '\\' + file, beam_index=5)
        result.pop(0)
        if len(result) <= 10:
          results[dir + '\\' + file] = ' '.join(result)
  return results

from flask import Flask, jsonify, request, url_for
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_url_path='/output', static_folder='output')  
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

UPLOAD_FOLDER = "E:\\CaptUploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')  
@cross_origin()
def upload():  
    return render_template("upload.html")
 
@app.route('/success', methods = ['POST'])  
@cross_origin()
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        b = request.form.get('beam_index')

        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))  
        extract_frames(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        cluster_frames('extracted_frames')
        drop_frames('output')

        results = {}
        capts_b = {}
        capts_br = {}
        res_b = []
        res_br = []

        x = [x[0] for x in os.walk('output')]
        for dir in x[1:]:
            files = os.listdir(dir)
            for file in files:
              cd = dir + '\\' + file
              result_b, _ = evaluate_beam_search(cd, beam_index=int(b))
              result_br, _ = evaluate_brute_force(cd)
              result_b.pop(0)
              # if len(result_b) <= 10 and len(result_br):
              capts_b[('http://localhost:5000/' + cd).replace('\\', '/')] = ' '.join(result_b)
              capts_br[('http://localhost:5000/' + cd).replace('\\', '/')] = ' '.join(result_br)
              res_b.append(' '.join(result_b))
              res_br.append(' '.join(result_br))

        res_b[0] = res_b[0].capitalize()
        res_br[0] = res_br[0].capitalize()

        results['beam_search_' + b] = capts_b
        results['beam_search_caption'] = ', '.join(res_b)

        results['brute_force'] = capts_br
        results['brute_force_caption'] = ', '.join(res_br)

        #os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        return jsonify(results)
        #return render_template("success.html", name = r2, url=os.path.join(app.config['UPLOAD_FOLDER'], f.filename))  

if __name__ == '__main__':  
    app.run(debug = True)  

    parser = argparse.ArgumentParser(description="Caption Videos.")
    parser.add_argument("-i", "--input", help="Your input video file.")
    parser.add_argument("-o", "--output", help="Your destination output file.")
    args = parser.parse_args()
    print(args.input)

    extract_frames(args.input)
    cluster_frames('extracted_frames')
    drop_frames('output')
    print(get_captions('output'))