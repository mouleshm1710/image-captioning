import streamlit as st
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array 
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical 
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np
from PIL import Image,ImageOps

@st.cache(allow_output_mutation=True)
def load_Model():
    model = load_model('my_model_8214_latest.h5')
    return model
with st.spinner('Model is being loaded..'):
     model=load_Model()
cnn_model = load_model('my_model_cnn.h5')

pickle_wi = open("wordtoixlatest.pkl", 'rb')
wordtoix = pickle.load(pickle_wi)

pickle_iw = open("ixtowordlatest.pkl", 'rb')
ixtoword = pickle.load(pickle_iw)

html_temp = """<div style ="background-color:#ff0099;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Image Captioner App</h1> 
    </div>"""

# display the front end aspect
st.markdown(html_temp, unsafe_allow_html = True)

# function define
def encode(image_path): 
    size = (224,224)    
    x = ImageOps.fit(image_path,size, Image.ANTIALIAS)
    y = np.asarray(x)
    y = np.expand_dims(y, axis=0) # expanding the 3rd dimension (1,224,224)
    y = preprocess_input(y)  # pixel values transform (NORMALIZATION) 
    fea_vec = cnn_model.predict(y) # returns the feature vector
    return fea_vec 

max_length = 20
def greedySearch(photo):                                                               
      in_text = 'sos'      
    
      for i in range(max_length):   

            sequence = [wordtoix[w] for w in in_text.split() if w in wordtoix] 
        
            sequence = pad_sequences([sequence], maxlen = max_length,padding = 'post',truncating = 'post')  
        
            yhat = model.predict([photo,sequence],verbose=0)    
             #print(yhat)
            yhat_val = np.argmax(yhat) 
             #print(yhat_val) 
            word = ixtoword[yhat_val]   
             #print(word) 
            in_text += ' ' + word
            
            if word == 'eos': 
                break
        
      final = in_text.split()
      final = final[1:-1]
      final = ' '.join(final)   
      return final 
    
img_file = st.file_uploader('', type=["jpg", "png","jpeg"])
if img_file is not None:
   img = Image.open(img_file)
   st.image(img,use_column_width=False)
    
else:
   pass
    
def main():
    try:
        feature_vector = encode(img)
        caption = greedySearch(feature_vector) 
        st.success("Hurray :)  we got the caption")
        st.success(caption)
    except:
        st.text("Please upload an image")
        
if __name__ == "__main__":              
    main()
