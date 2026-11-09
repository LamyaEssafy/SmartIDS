import streamlit as st
import pickle

model=pickle.load(open('model.pkl','rb'))

def classify(num):
    if num>0:
        return '1 : Kecimen' 
    else:
        return '0 : Besni'
def main():
    html_temp = """
    <style>
    .appview-container .main .block-container{{
        max-width: "200px";
    }}
    .reportview-container .main {{
        color: white;
        background-color: grey;
    }}
    </style>
    <div style="background-color:teal ;padding:10px">
    <h3 style="font-size:18pt;color:white;text-align:center;">Raisin Classification (0 : Besni | 1 : Kecimen)</h3>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    # Params = Area - MajorAxisLength - MinorAxisLength - Eccentricity - ConvexArea - Extent - Perimeter
    Area=st.slider('Select Area', 0.0, 1.0)
    MajorAxisLength=st.slider('Select MajorAxisLength', 0.0, 1.0)
    MinorAxisLength=st.slider('Select MinorAxisLength', 0.0, 1.0)
    Eccentricity=st.slider('Select Eccentricity', 0.0, 1.0)
    ConvexArea=st.slider('Select ConvexArea', 0.0, 1.0)
    Extent=st.slider('Select Extent', 0.0, 1.0)
    Perimeter=st.slider('Select Perimeter', 0.0, 1.0)
    inputs=[[Area,MajorAxisLength,MinorAxisLength,Eccentricity,ConvexArea,Extent,Perimeter]]
    if st.button('Classify'):
        st.success(classify(model.predict(inputs)))


if __name__=='__main__':
    main()