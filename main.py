import os 
from app import app 
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from PIL import Image, ImageChops, ImageFilter, ImageDraw

ALLOWED_EXTENSION = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSION

@app.route('/')
def upload_form():
   return render_template('index.html')

@app.route('/', methods = ['POST'])
def upload_image():
   if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
   file = request.files['file']
   print(file.filename)
   slider = request.form['enterRange']
   if file.filename == '':
      flash('No image selected for uploading')
   if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      fName = filename.split('.')[0]
      ext = filename.split('.')[1]
      filename = fName + '.png'
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      inputImage = './Static/Uploads/' + filename
      baseImage = './Static/Uploads/' + filename
      inp = Image.open(inputImage)
      base = Image.open(baseImage)
      flash(inp.size[0])
      inp = inp.convert("RGBA")
      base = base.convert("RGBA")
      width, hieght = inp.size
      black = (0, 0, 0)

      sens = int(slider)

      pixel = inp.load()
      basePix = base.load()

      colors = []

      ranges = []


      for row in range(inp.size[0]):
         for column in range(0, 3):
             if pixel[row, column] not in colors:
               colors.append(pixel[row, column])


      for row in range(inp.size[0]):
         for column in range(inp.size[1]):
            newColor = basePix[row, column]
            for color in colors:
               target = pixel[row, column]
               if checkPixel(target, color, sens):
                  pixel[row, column] = (255, 255, 255, 0)
               else:
                  pixel[row, column] = (0, 0, 255, 255)

      ImageDraw.floodfill(inp, (0, 0), (255, 0, 0, 255))


      for row in range(inp.size[0]):
         for column in range(inp.size[1]):
            newColor = basePix[row, column]
            if pixel[row, column] == (255, 0, 0, 255):
               pixel[row, column] = (0, 0, 0, 0)
            else:
               pixel[row, column] = newColor

      inp.save('./Static/Uploads/' + filename)
      flash('Image successfully uploaded')
      return send_file('./Static/Uploads/' + filename)
      #return render_template('index.html', filename='Input.png')


@app.route('/display/<filename>')
def display_image(filename):
   print('display_image filename: ' + filename)
   return redirect(url_for('static', filename='uploads/' + filename), code=301)


def checkPixel(target, color, sen):
    if target[0] >= max(color[0] - sen, 0) and target[1] >= max(color[1] - sen, 0) and target[2] >= max(color[2] - sen, 0):
        if target[0] <= min(color[0] + sen, 255) and target[1] <= min(color[1] + sen, 255) and target[2] <= min(color[2] + sen, 255):
            return True

if __name__ == "__main__":
    app.run()