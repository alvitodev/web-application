import streamlit as st
from PIL import Image

# Image
image = Image.open('./week-2/THUMBNAIL.png')
st.image(image, caption='Thumbnail review laptop di channel Alvito Dev')

# Audio
audio_file = open('./week-2/Calvin Harris - Feels (Official Video) ft. Pharrell Williams, Katy Perry, Big Sean - CalvinHarrisVEVO.mp3', 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/mp3')

# Video
video_file = open('./week-2/a21a64fe0131928e76bc9924aed2da8fccd5dfad.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes, format='video/mp4')
