# -*- coding: utf-8 -*-
"""streamlit-Subsid.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LDPHl0OhnakUhZwxq8c-pozVxTmqj5OE
"""

# !pip install pillow
# !pip install streamlit
# !pip install pyngrok

# !pip install streamlit -q
# !pip install spacy
# !pip install geopy
# !pip install pillow

"""
###to run the model and get the similarity check these 2 are important
"""

# !pip install flash_attn timm
# !python3 -m spacy download en_core_web_lg

"""###Writes the app.py and Streamlit is itegrated"""

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# import streamlit as st
# import torch
# from transformers import AutoModelForCausalLM, AutoProcessor
# import spacy
# from geopy.geocoders import Nominatim
# from PIL import Image
# import json
# 
# 
# nlp = spacy.load("en_core_web_lg")
# 
# 
# model_id = 'microsoft/Florence-2-large'
# model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, torch_dtype='auto').eval().cuda()
# processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
# 
# def run_example(task_prompt, image, text_input=None):
#     if text_input is None:
#         prompt = task_prompt
#     else:
#         prompt = task_prompt + text_input
#     inputs = processor(text=prompt, images=image, return_tensors="pt").to('cuda', torch.float16)
#     generated_ids = model.generate(
#         input_ids=inputs["input_ids"].cuda(),
#         pixel_values=inputs["pixel_values"].cuda(),
#         max_new_tokens=1024,
#         early_stopping=False,
#         do_sample=False,
#         num_beams=3,
#     )
#     generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
#     parsed_answer = processor.post_process_generation(
#         generated_text,
#         task=task_prompt,
#         image_size=(image.width, image.height)
#     )
#     return parsed_answer
# 
# def compare_text_similarity(text1, text2):
#     s1 = nlp(text1)
#     s2 = nlp(text2)
#     similarity = s1.similarity(s2)
#     if similarity >= 0.98:
#         return "Both images are similar", similarity
#     else:
#         return "Images are not similar", similarity
# 
# 
# st.title("Subsidy Verification System")
# 
# role = st.selectbox("Are you an admin or farmer?", ("Admin", "Farmer"))
# 
# if role == "Admin":
#     st.header("Admin Section")
#     admin_id = st.text_input("Enter Admin ID")
#     subsidy_id = st.text_input("Enter Subsidy ID")
#     farmer_id = st.text_input("Enter Farmer ID")
#     uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
# 
#     if st.button("Process Image"):
#         if uploaded_image:
#             image = Image.open(uploaded_image)
#             image = processor(images=image).pixel_values
#             caption = run_example('<DETAILED_CAPTION>', image)
#             st.write("Generated Caption:", caption)
#             st.success("Image has been successfully processed and caption generated.")
# 
# 
#             # Temporary storag
#             # you cna connect to database later
#             data = {
#                 "admin_id": admin_id,
#                 "subsidy_id": subsidy_id,
#                 "farmer_id": farmer_id,
#                 "caption": caption
#             }
# 
# 
#             with open('admin_data.json', 'w') as f:
#                 json.dump(data, f)
# 
#             st.write("Data temporarily stored in 'admin_data.json'. You can later move this to a database.")
# 
# elif role == "Farmer":
#     st.header("Farmer Section")
#     farmer_id = st.text_input("Enter Farmer ID")
#     subsidy_id = st.text_input("Enter Subsidy ID")
#     uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
# 
#     if st.button("Verify and Process"):
#         if not farmer_id:
#             st.error("Please enter your Farmer ID.")
#         elif not subsidy_id:
#             st.error("Please enter the Subsidy ID.")
#         elif not uploaded_image:
#             st.error("Please upload an image.")
#         else:
#             try:
#                 with open('admin_data.json', 'r') as f:
#                     admin_data = json.load(f)
# 
#                 admin_caption = admin_data['caption'] if admin_data['subsidy_id'] == subsidy_id else None
# 
#                 if admin_caption:
#                     image = Image.open(uploaded_image)
#                     image = processor(images=image).pixel_values
#                     farmer_caption = run_example('<DETAILED_CAPTION>', image)
#                     st.write("Admin Image Text:", admin_caption)
#                     st.write("Farmer Image Text:", farmer_caption)
#                     result, similarity_score = compare_text_similarity(admin_caption, farmer_caption)
#                     st.write(result)
#                     st.write("Similarity Score:", similarity_score)
# 
#                     if similarity_score >= 0.98:
#                         st.success("Image accepted")
#                     else:
#                         st.error("Please upload a new image")
#                 else:
#                     st.error("No matching subsidy found for the provided ID.")
# 
#             except FileNotFoundError:
#                 st.error("Admin data not found. Please process an image as an admin first.")
#

# # Optional: Commented code for location fetching using geopy
# """
# geolocator = Nominatim(user_agent="geoapiExercises")

# def fetch_location():
#     loc = geolocator.geocode("Your location query here")
#     st.write("Farmer Location:", loc.address)
#     return loc.latitude, loc.longitude

# if st.checkbox("Fetch Location"):
#     if st.button("Get Location"):
#         latitude, longitude = fetch_location()
#         st.write("Latitude:", latitude, "Longitude:", longitude)
# """

"""###to run the web interface must have account in ngrok"""

ngrok.set_auth_token("<authtoken>")
!ngrok config add-authtoken <authtoken>
!streamlit run app.py&>/dev/null&
!pgrep streamlit

from pyngrok import ngrok
# Create a tunnel on port 5000
http_tunnel = ngrok.connect(8501,'http')
print("Public URL:", http_tunnel.public_url)