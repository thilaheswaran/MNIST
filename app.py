from flask import Flask, render_template, request
import pickle as pk
from PIL import Image
import numpy as np
from numpy import asarray
#from keras.preprocessing import image

app = Flask(__name__)

dic = {0 : 'Zero', 1 : 'One', 2:'Two', 3:'Three', 4:'Four', 5:'Five', 6:'Six', 7:'Seven', 8:'Eight', 9:'Nine'}

model = pk.load(open('model.pkl', 'rb'))

#model.make_predict_function()

def predict_label(img_path):

    i = Image.open(img_path).convert('RGBA')
    #i = asarray(i)
	#i = image.img_to_array(i)/255.0
    
    #im = Image.open('image.png')
    bg = Image.new('RGBA', i.size, (255,255,255))

    alpha = Image.alpha_composite(bg,i)
    # alpha = im
    alpha = alpha.convert('L')
    alpha = alpha.resize((28,28))

   


    image_np = np.array(alpha).reshape(784,)
    print(image_np)

    """i = i.reshape(784,1)
    print(i.shape)"""
    p = model.predict([image_np])
    return dic[p[0]]


# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")



@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		p = predict_label(img_path)

	return render_template("index.html", prediction = p, img_path = img_path)


if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)