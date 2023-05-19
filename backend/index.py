from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from ocr_handler import *
import os
from fpdf import FPDF
import time

#create a pdf file from .txt transcript file

############################################################
def pdfCreater():
  pdf = FPDF()  
  
# Add a page
  pdf.add_page()
  
# set style and size of font
# that you want in the pdf
  pdf.set_font("Arial", size = 15)
 
# open the text file in read mode
  f = open("transcript.txt", "r")
 
# insert the texts in pdf
  for x in f:
    pdf.cell(200, 10, txt = x, ln = 1, align = 'C')
  
  timestamp = time.strftime('%Y%m%d%H%M%S')
  output_file = f'output_file_{timestamp}.pdf'
# save the pdf with name .pdf
  pdf.output(output_file)  

###############################################################################################
# pdf converter ends here

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'
       
@app.route('/upload', methods=['POST'])
def upload_video():
    file = request.files['video']
    print(file)
    if file:
        filename = file.filename
        file.save(os.path.join(app.root_path, 'uploads', filename))
        video_file_name = 'uploads/'+filename
        print(video_file_name)
        ocr_handler = OCR_HANDLER(video_file_name, CV2_HELPER(),"LINES")
        if os.path.exists('transcript.txt'):
          print("hello")
          os.remove('transcript.txt')
        
        ocr_handler.process_frames()
        ocr_handler.assemble_video()
        print("OCR PROCESS FINISHED: OUTPUT FILE => " + ocr_handler.out_name)
        
        with open('transcript.txt', 'r') as file:
         text = file.read().replace('\n', ' ')
        print(text)
        return jsonify(text=text)
    else:
        return jsonify({'error': 'No video file provided.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
