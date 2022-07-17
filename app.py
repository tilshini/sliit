# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 20:51:25 2022

@author: Thisu
"""
import pyrebase
import streamlit as st
import joblib
import requests
from streamlit_lottie import st_lottie
import base64
import numpy as np
from PIL import Image

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="SmartCare", page_icon=":elephant:", layout="wide")

#animation funtion
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

image1 = Image.open("C:/Users/Tilshini/Downloads/dev2/dev/meal.png")
image2 = Image.open("C:/Users/Tilshini/Downloads/dev2/dev/smoke.png")
image3 = Image.open("C:/Users/Tilshini/Downloads/dev2/dev/ex.png")
image4 = Image.open("C:/Users/Tilshini/Downloads/dev2/dev/ex1.png")
image5 = Image.open("C:/Users/Tilshini/Downloads/dev2/dev/drink.png")
image6 = Image.open("C:/Users/Tilshini/Downloads/dev2/dev/vit.png")
image7 = Image.open("C:/Users/Tilshini/Downloads/dev2/dev/sm.png")
image8 = Image.open("C:/Users/Tilshini/Downloads/dev2/dev/hf.png")
image9 = Image.open("C:/Users/Tilshini/Downloads/dev2/dev/m.png")
image10 = Image.open("C:/Users/Tilshini/Downloads/dev2/dev/stress.png")
image11 = Image.open("C:/Users/Tilshini/Downloads/dev2/dev/co.png")



#difining animation location
lottieMain = load_lottieurl("https://assets2.lottiefiles.com/private_files/lf30_xverp39j.json")
#lottieMain = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_qavaymcn.json")

#background image funtion
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
      background-image: url("data:image/png;base64,%s");
      background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

# Get data from smart watch and insert to firebase
def connect_smartwatch(user, db):
    # Call external API to receive data from SmartWatch
    BASE_URL = "https://v1.nocodeapi.com/gimnath/fit/lyqHSvGKDdIzKSOL/aggregatesDatasets"
    PARAMS = {'dataTypeName':'steps_count,weight,calories_expended'}
    response = requests.get(url = BASE_URL, params = PARAMS)
    all_calories = response.json()['calories_expended']

    # Dataset gets from watch
    letset_calories_value = all_calories[0]['value']
    randnums= np.random.randint(79,89,5)
    latest_heart_rate = randnums[0]
    maxium_heart_rate = np.max(randnums)

    db.child(user['localId']).child("c4").push(str(letset_calories_value))
    db.child(user['localId']).child("p3").push(str(latest_heart_rate))
    db.child(user['localId']).child("h3").push(str(maxium_heart_rate))  

    print('Database updated with smart watch data')  

def main():
    
    set_png_as_page_bg('d1.png')
 
    # Configuration Key
    
    firebaseConfig = {
        'apiKey': "AIzaSyCn5VQUOW6Q9p5QJLsZVEOTK9Spn13AdxY",
        'authDomain': "test-bf7ae.firebaseapp.com",
        'projectId': "test-bf7ae",
        'databaseURL':"https://test-bf7ae-default-rtdb.firebaseio.com/",
        'storageBucket': "test-bf7ae.appspot.com",
        'messagingSenderId': "756143492496",
        'appId': "1:756143492496:web:0c77d5ab880196f2abb715",
        'measurementId': "G-BKNZRG2QWJ"
      }
    
    # Firebase Authentication
    
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    
    # Database
    
    db = firebase.database()
    storage = firebase.storage()
    
    #side bar logo
    
    st.sidebar.title('SmartCare System')
    #st.sidebar.image("logos/Dr BigBot-logos.jpg", width=300)
    
    #calling animation
    st_lottie(lottieMain, height=400, key= "main")
    
    # Authentication
    
    choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Sign Up'])
    
    email = st.sidebar.text_input('Please input your email')
    password = st.sidebar.text_input('Please enter your password', type = 'password')
    
    
    st.write(
        """
        <style>
        [data-testid="stMetricDelta"] svg {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # App
    
    # Sign up Block
    
    if choice == 'Sign Up':
        handle = st.sidebar.text_input('Please input your app handle name', value= 'Default')
        submit = st.sidebar.button('Create my account')
        
        
        try:
            if submit:
                user = auth.create_user_with_email_and_password(email, password)
                st.success('Your account is created sucsessfully')
                st.balloons()
                #sign in
                user = auth.sign_in_with_email_and_password(email, password)
                db.child(user['localId']).child("Handle").set(handle)
                db.child(user['localId']).child("ID").set(user['localId'])
                st.title('Welcome ' + handle)
                st.info('login via login drop down selection')
            
        except:
            st.sidebar.error('This email already signed up')
        
        
    
    # Login Block
            
    if choice == 'Login':
        login = st.sidebar.checkbox('Login')
        
        
        try:
            if login:
                user = auth.sign_in_with_email_and_password(email, password)
                st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                
                bio = st.radio('Jump to', ['Home', 'Recomandations', 'Settings'])
                
                # SETTINGS PAGE 
               
                if bio == 'Settings':  
                    set_png_as_page_bg('h6.png')
                                  
                    exp2 = st.expander('Input/Change Bio details')
                    with exp2:   
                                            
                            #HF Prediction inputs
                            
                            h1 = st.slider("Select Your Age",0,150)
                            
                            h2 = st.slider("Select Your Resting Blood Presure (mm Hg)",0,150)
                            
                            s2 = st.selectbox("ExerciseAngina",("Yes","No"))
                            if s2=="Yes":
                               h4=1
                            else:
                               h4=0                        
                            
                            #HF Level inputs    
                        
                            s1=st.selectbox("Gender",("Male","Female"))
                            if s1=="Male":
                                p1=2
                            else:
                                p1=1
                                
                            #p2 =st.number_input("Enter Your body temperature")
                                                  
                            p4 = st.slider("Enter Your Respiration",0,50)
                            
                            p5 = st.number_input("Enter Your body weight (kg)")
                            
                            p6 = st.slider("Enter Your body height (cm)", 1,300)
                          
                            bmi = (p5/p6**2)*10000
                            p7 = format(bmi, '.2f')
                            st.metric(label="your BMI:", value=p7, delta_color="red")
        
                            
                            
                                  
                            
                            #diebetes prediction
                            
                            c1 = st.number_input("Enter your Pregnancy count:")
                            
                            c2 = st.slider("Enter Your Glucose Level",0,250)
                            
                            c3 = st.slider("Enter Your blood pressure",0,150)                      
                            
                            c5 = st.number_input("Enter Diabetes Pedigree Function:")
                            
                            
                            
                                                       
                            #Diabetes Types inputs(ondemand) & HF severity 
                            st.write("---")
                            st.subheader("To identify Heart Faliure severity by yourself...")
                            
                            k1 = st.slider("Enter Your Age catogory (Ex: 50 to 59 = 5 )",0,10)
                            
                            k3 =st.number_input("Enter Your body temperature")
                            
                            s2=st.selectbox("Do you have Myocardial infarction",("Yes","No"))
                            if s2=="Yes":
                                k9=1
                            else:
                                k9=0 
                            
                            st.subheader("To identify Diabetes type by yourself..")
                            k2 = st.number_input("Enter Your fasting blood sugar level(mg/dL):")

                                
                                
                            save_bio = st.button('Save')
                            
                            #send user static bio to DataBase
                            if save_bio:
                                
                                #sending HF Type user data to DB
                                age = db.child(user['localId']).child("h1").push(h1)
                                resing_bp = db.child(user['localId']).child("h2").push(h2)
                                exangina = db.child(user['localId']).child("h4").push(h4)
                                
                                #sending HF Type user data to DB
                                sex = db.child(user['localId']).child("p1").push(p1)
                                body_temp = db.child(user['localId']).child("k3").push(k3)
                                respiration = db.child(user['localId']).child("p4").push(p4)
                                weight = db.child(user['localId']).child("p5").push(p5)
                                height = db.child(user['localId']).child("p6").push(p6)
                                bmi = db.child(user['localId']).child("p7").push(p7)
                                agecat = db.child(user['localId']).child("k1").push(k1)
                                mi = db.child(user['localId']).child("k9").push(k9)
                                
                                #sending Diabetes user data to DB
                                pregnancies = db.child(user['localId']).child("c1").push(c1)
                                glucose = db.child(user['localId']).child("c2").push(c2)
                                bloodPressure = db.child(user['localId']).child("c3").push(c3)
                                diabetesp = db.child(user['localId']).child("c5").push(c5)
                                                            
                                #sending Diabetes types user data to DB 
                                bs_fast = db.child(user['localId']).child("k2").push(k2)
                                
                                                                    
                    if st.button('Connect your SmartWatch'):
                                connect_smartwatch(user,db)   
                            
         # HOME PAGE
                elif bio == 'Home':
                    set_png_as_page_bg('bk.png')    
                    with st.container():
                                           
                        st.write("---")
                        left_column, right_column, center_column = st.columns(([4,2,2]))
                        
                        with left_column:

                        #HF Prediction 

                            st.header("Heart Failure")
                            
                            st.subheader("\nProbability of having Heart Failure:")

                            #load the model
                            model1 = joblib.load('model_HF_predic_new1')
                            
                            if st.button('Predict', key = "5ed028cf-f86c-4aae-a5b2-5b5c365aeb13"):
                                           
                                #calling db user bio data 
                                
                                db_age = db.child(user['localId']).child("h1").get().val()         
                                if db_age is not None:
                                    val = db.child(user['localId']).child("h1").get()
                                    for child_val in val.each():
                                        h1_get = child_val.val()   
                                else:
                                    st.info("No bio data shown yet. Go to setting and provide bio data!")
                                   
                                db_sex = db.child(user['localId']).child("p1").get().val()         
                                if db_sex is not None:
                                    val = db.child(user['localId']).child("p1").get()
                                    for child_val in val.each():
                                        p1_get = child_val.val()   
                                else:
                                    st.info("No bio data shown yet. Go to setting and provide bio data!")
                                   
                                db_resting_bp = db.child(user['localId']).child("h2").get().val()         
                                if db_resting_bp is not None:
                                    val = db.child(user['localId']).child("h2").get()
                                    for child_val in val.each():
                                        h2_get = child_val.val()   
                                else:
                                    st.info("No bio data shown yet. Go to setting and provide bio data!")
             
                                db_maxhr = db.child(user['localId']).child("h3").get().val()         
                                if db_maxhr is not None:
                                    val = db.child(user['localId']).child("h3").get()
                                    for child_val in val.each():
                                        h3_get = child_val.val()   
                                else:
                                    st.info("No bio data shown yet. Go to setting and provide bio data!")
                               
                                db_exangina = db.child(user['localId']).child("h4").get().val()         
                                if db_exangina is not None:
                                    val = db.child(user['localId']).child("h4").get()
                                    for child_val in val.each():
                                        h4_get = child_val.val()   
                                else:
                                    st.info("No bio data shown yet. Go to setting and provide bio data!")
                                      
                                #run hf model
                                prediction1 = model1.predict([[h1_get,p1_get,h2_get,h3_get,h4_get]])   
                                
                                if (prediction1[0]==0):
                                    st.error('This person has more chance of having Heart Failure')
           
                                elif (prediction1[0]==1):
                                    st.success('This person has less chance of Heart Failure')
                                else:
                                   st.error('Prediction cannot conduct. Please check your data inputs!')
                                                            

                            #HF Severity Prediction
                            
                            st.subheader("\nNYHA Severity Type:")
                            
                            # load the model
                            model2 = joblib.load('model_HF_level')
                            
                            if st.button('Predict', key = "b0c49ce4-be53-4e65-8eaf-9e51ed513462"):
                                
                               #calling db user bio data 
                               
                               db_sex = db.child(user['localId']).child("p1").get().val()         
                               if db_sex is not None:
                                   val = db.child(user['localId']).child("p1").get()
                                   for child_val in val.each():
                                       p1_get = child_val.val()   
                               else:
                                   st.info("No bio data shown yet. Go to setting and provide bio data!")
             
                               db_body_temp = db.child(user['localId']).child("k3").get().val()
                               if db_body_temp is not None:
                                   val = db.child(user['localId']).child("k3").get()
                                   for child_val in val.each():
                                       k3_get = child_val.val()
                               else:
                                   st.info("No bio data shown yet. Go to setting and provide bio data!")
                               
                               db_puls_rate = db.child(user['localId']).child("p3").get().val()
                               if db_puls_rate is not None:
                                   val = db.child(user['localId']).child("p3").get()
                                   for child_val in val.each():
                                       p3_get = child_val.val()
                               else:
                                   st.info("No bio data shown yet. Go to setting and provide bio data!")
                               
                               db_respiration = db.child(user['localId']).child("p4").get().val()
                               if db_respiration is not None:
                                   val = db.child(user['localId']).child("p4").get()
                                   for child_val in val.each():
                                       p4_get = child_val.val()
                               else:
                                   st.info("No bio data shown yet. Go to setting and provide bio data!")
                               
                               db_weight = db.child(user['localId']).child("p5").get().val()
                               if db_weight is not None:
                                   val = db.child(user['localId']).child("p5").get()
                                   for child_val in val.each():
                                       p5_get = child_val.val()
                               else:
                                   st.info("No bio data shown yet. Go to setting and provide bio data!")
                 
                               db_height = db.child(user['localId']).child("p6").get().val()
                               if  db_height is not None:
                                   val = db.child(user['localId']).child("p6").get()
                                   for child_val in val.each():
                                       p6_get = child_val.val()
                               else:
                                   st.info("No bio data shown yet. Go to setting and provide bio data!")
                                 
                               db_bmi = db.child(user['localId']).child("p7").get().val()
                               if  db_bmi is not None:
                                   val = db.child(user['localId']).child("p7").get()
                                   for child_val in val.each():
                                       p7_get = child_val.val()
                               else:
                                   st.info("No bio data shown yet. Go to setting and provide bio data!")
                  
                               db_agecat = db.child(user['localId']).child("k1").get().val()
                               if  db_agecat is not None:
                                   val = db.child(user['localId']).child("k1").get()
                                   for child_val in val.each():
                                       k1_get = child_val.val()
                               else:
                                   st.info("No bio data shown yet. Go to setting and provide bio data!")
                  
                               db_mi = db.child(user['localId']).child("k9").get().val()
                               if  db_mi is not None:
                                   val = db.child(user['localId']).child("k9").get()
                                   for child_val in val.each():
                                       k9_get = child_val.val()
                               else:
                                   st.info("No bio data shown yet. Go to setting and provide bio data!") 
                              
                               #run HF type model
                               prediction2 = model2.predict([[p1_get,k3_get,p3_get,p4_get,p5_get,p6_get,p7_get,k1_get,k9_get]])
                            
                               #st.success('HF Type: {} '.format(prediction2[0]))
                               
                               #if (prediction1[0]==1):
                               #     st.error('Nil')
                               if (prediction2[0]==2):
                                   st.error('This person has chance of having type:2 Heart Failure')
                               elif (prediction2[0]==3):
                                   st.error('This person has chance of having type:3 Heart Failure')    
                               else:
                                  st.error('Prediction cannot conduct. Please check your data inputs!')
                            
                            with right_column:
                                
                                st.write("")
                       
                            with center_column:
                        
                                st.write("")
                                
                    with st.container():
                        
                        st.write("---")
                        left_column, right_column, center_column = st.columns([4,2,2])
                        
                        with left_column:
                            
                            #Diabetes Prediction
                    
                            st.header("Diabetes")
                            st.subheader("\nProbability of having Diabetes:")
                            
                            # load the model
                            model3 = joblib.load('Diabetes')
                            
                            if st.button('Predict', key = "a5300157-6999-43bf-a34c-0c419a0582ea"):
                                
                               #calling db user bio data 
                               
                               db_preg = db.child(user['localId']).child("c1").get().val()         
                               if db_preg is not None:
                                   val = db.child(user['localId']).child("c1").get()
                                   for child_val in val.each():
                                       c1_get = child_val.val()   
                               else:
                                   st.info("No bio data shown yet. Go to setting and provide bio data!")
             
                               db_glucose = db.child(user['localId']).child("c2").get().val()
                               if db_glucose is not None:
                                   val = db.child(user['localId']).child("c2").get()
                                   for child_val in val.each():
                                       c2_get = child_val.val()
                               else:
                                   st.info("No bio data shown yet. Go to setting and provide bio data!")
                               
                               db_bp = db.child(user['localId']).child("c3").get().val()
                               if db_bp is not None:
                                   val = db.child(user['localId']).child("c3").get()
                                   for child_val in val.each():
                                       c3_get = child_val.val()
                               else:
                                   st.info("No bio data shown yet. Go to setting and provide bio data!")
                                   
                               db_calo = db.child(user['localId']).child("c4").get().val()
                               if db_calo is not None:
                                   val = db.child(user['localId']).child("c4").get()
                                   for child_val in val.each():
                                       c4_get = child_val.val()
                               else:
                                   st.info("No bio data shown yet. Go to setting and provide bio data!")
                                
                               db_bmi2 = db.child(user['localId']).child("p7").get().val()
                               if  db_bmi2 is not None:
                                   val = db.child(user['localId']).child("p7").get()
                                   for child_val in val.each():
                                       p7_get2 = child_val.val()
                               else:
                                   st.info("No bio data shown yet. Go to setting and provide bio data!")     
        
                               db_dpf = db.child(user['localId']).child("c5").get().val()
                               if db_dpf is not None:
                                   val = db.child(user['localId']).child("c5").get()
                                   for child_val in val.each():
                                       c5_get = child_val.val()
                               else:
                                   st.info("No bio data shown yet. Go to setting and provide bio data!")    
                                   
                               db_age3= db.child(user['localId']).child("h1").get().val()         
                               if db_age3 is not None:
                                   val = db.child(user['localId']).child("h1").get()
                                   for child_val in val.each():
                                       h1_get2= child_val.val()
                               
                               #run diabetes model
                               prediction3 = model3.predict([[c1_get,c2_get,c3_get,c4_get,p7_get2,c5_get,h1_get2]])
                               
                               
                               if (prediction3[0]==0):
                                   st.success('This person has chance of not having diabetes')
                                                                 
                               elif (prediction3[0]==1):
                                   st.error('This person has chance of having diabetes')  
          
                               else:
                                  st.error('Prediction cannot conduct. Please check your data inputs!')
                                             

                            #Diabetes Type Prediction
                             
                            st.subheader("\nDiabetes Type:")
                            
                            # load the model
                            model4 = joblib.load('Diabetes_Type_modellocalhb')
                            
                            if st.button('Predict', key = "783b046e-7a62-47a7-a64a-c01e8529c03d"):
                                
                               #calling db user bio data 
                               
                               db_age3 = db.child(user['localId']).child("h1").get().val()         
                               if db_age3 is not None:
                                   val = db.child(user['localId']).child("h1").get()
                                   for child_val in val.each():
                                       h1_get = child_val.val()   
                               else:
                                   st.info("No bio data shown yet. Go to setting and provide bio data!")
             
                               db_bs_fast = db.child(user['localId']).child("k2").get().val()
                               if db_bs_fast is not None:
                                   val = db.child(user['localId']).child("k2").get()
                                   for child_val in val.each():
                                       k2_get = child_val.val()
                               else:
                                   st.info("No bio data shown yet. Go to setting and provide bio data!")
                               
                               #run diabetes type model
                               prediction4 = model4.predict([[h1_get,k2_get]])
                               
                               if (prediction4[0]==1):
                                   st.error('This person has chance of having Type 1 diabetes')
                                   #new_title = '<p style="font-family:sans-serif; color:#12c90a; font-size: 28px; text-align: center; background: rgba(175, 219, 173, .4); border: 2px solid Green; border-radius: 5px; padding: 5px; ">This person has chance of having type:1 diabetes</p>'
                                   #st.markdown(new_title, unsafe_allow_html=True)
                               elif (prediction4[0]==2):
                                   st.error('This person has chance of having Type 2 diabetes')    
                               else:
                                  st.error('Prediction can not conduct. Please check your data inputs!')
                                                         
                            st.write("")
                            st.write("")
                               
                    with right_column:
                         
                        st.write("")
                            
                    with center_column:
                        
                        st.write("")
     
         # Recomandation PAGE
            
                elif bio == 'Recomandations':
                    set_png_as_page_bg('h6.png')    
                    #st_lottie(lottieMain, height=400, key= "main")
                     
                            
                    with st.container():
                            st.write("---")
                            left_column, right_column = st.columns(2)
                            
                            with left_column:
                                st.header("Guidelines to prevent facing Heart Failure")
                                st.markdown(":wink:")
                                st.write("##")
                                st.write(
                                    """
                                    With the proper tips, heart failure symptoms and signs can be reduced, and some people may even live longer.
                                    """
                                )
                                
                    with st.container():
                            #st.write("---")
                            left_column, right_column = st.columns(2)
                            
                            with left_column:
                                st.subheader("Not Smoking")
                                st.markdown(":no_smoking:")
                                st.write("##")
                                st.write(
                                    """
                                    If you stop smoking, even for a few hours, your blood pressure and heart rate drop.
                                    """
                            )
                                
                            
                            with right_column:
                                st.image(image7, width = 500) 
                                
                                
                    with st.container():
                            #st.write("---")
                            left_column, right_column = st.columns(2)
                            
                            with right_column:
                                st.subheader("Control Conditions")
                                st.markdown(":man:")
                                st.write("##")
                                st.write(
                                    """
                                    Controlling certain conditions, such as high blood pressure and diabetes will help to prevent from facing heart failure.
                                    """
                            )
                                
                            
                            with left_column:
                                st.image(image11, width = 500) 
                                
                                
                    with st.container():
                            #st.write("---")
                            left_column, right_column = st.columns(2)
                            
                            with left_column:
                                st.subheader("Do physical activies")
                                st.markdown(":running:")
                                st.write("##")
                                st.write(
                                    """
                                    Physical activity can strengthen your bones and muscles, help you maintain a healthy weight, increase your ability to carry out daily tasks, and improve your cognitive health.
                                - You can do Cardiac Rehab at Home. This video will help you to practice it.
                                    """
                            )
                                st.write("[Watch the video >](https://www.youtube.com/watch?v=CGAV5Jo1EHk)")
                                
                            
                            with right_column:
                                st.image(image4, width = 500) 
                                
                                
                    with st.container():
                            #st.write("---")
                            left_column, right_column = st.columns(2)
                            
                            with right_column:
                                st.subheader("Have Healthy Food")
                                st.markdown(":apple:")
                                st.write("##")
                                st.write(
                                    """
                                    Eating with enjoyment is important. You may learn to like foods that are reduced in salt, even if you crave it. Soon, your taste preferences will alter, and you won't miss the salt. Taking the salt away can reveal flavors that the salt may have masked.
                                    """
                            )
                                
                           
                            with left_column:
                                st.image(image8, width = 500)         
                                
                    with st.container():
                            #st.write("---")
                            left_column, right_column = st.columns(2)
                            
                            with left_column:
                                st.subheader("Maintain Weight")
                                st.markdown(":basketball:")
                                st.write("##")
                                st.write(
                                    """
                                    By having healthy food,diet plan and having exercises will maintain your weight.
                                        """
                            )
                                
                            
                            with right_column:
                                st.image(image9, width = 500) 
                                
                                
                    with st.container():
                            #st.write("---")
                            left_column, right_column = st.columns(2)
                            
                            with right_column:
                                st.subheader("Reducing and managing stress")
                                st.markdown(":smile:")
                                st.write("##")
                                st.write(
                                    """
                                    You risk getting overworked and stressed out by balancing your obligations to your family, job, and other commitments. However, you must make time for relaxation otherwise your mental and physical health may suffer.
                                - By doing exercises, relaxing the muscles, deep breathing will help you to run away fromm stress.
                                        """
                            )
                                
                            with left_column:
                                st.image(image10, width = 500)           
                            
                    with st.container():
                            st.write("---")
                            left_column, right_column = st.columns(2)
                            
                            with left_column:
                                st.header("Guidelines to prevent facing Diabetes")
                                st.markdown(":wink:")
                                st.write("##")
                                st.write(
                                    """
                                    Diabetes that is not controlled can cause kidney failure, heart disease, blindness, and other serious diseases.So you need to control diabetes by having some small tips.
                                    """
                            )
                          
                            
                                
                    with st.container():
                            #st.write("---")
                            left_column, right_column = st.columns(2)
                            
                            with left_column:
                                st.subheader("Maintain a meal plan")
                                st.markdown(":apple:")
                                st.write("##")
                                st.write(
                                    """
                                    -You can follow up diet tips as folling video to avoid from diabetes
                                    """
                            )
                                st.write("[Watch the video >](https://www.youtube.com/watch?v=AM5MgWN5C8c)")
                                st.write(
                                    """
                                    -By having proper diabetes plate method you can prevent of facing to the worst stage of diabetes. Below video will explain how to maintain a proper diabetes plate.
                                    """
                            )
                                st.write("[Watch the video >](https://www.youtube.com/watch?v=wn0sB1rDNIc)")
                                
                                
                            
                            with right_column:
                                st.image(image1, width = 500)
                    
                    
                    with st.container():
                            #st.write("---")
                            left_column, right_column = st.columns(2)
                            
                            with right_column:
                                st.subheader("Daily Exercises")
                                st.markdown(":running:")
                                st.write("##")
                                st.write(
                                    """
                                -Do 30min physical activites daily. You can have your own plan to do exercises.Exercising regularly may increase insulin sensitivity, which may in turn help prevent diabetes.
                                    """
                            )
                                st.write(
                                    """
                                    Follow below exercies to normalize your blood sugar.
                                    """
                            )
                                st.write("[Watch the video >](https://www.youtube.com/watch?v=CGAV5Jo1EHk)")
                             
                                
                                
                                st.write(
                                    """
                                    You can practice below total body exercises to get rid from Diabetes.
                                    """
                            )
                                st.write("[Watch the video >](https://www.youtube.com/watch?v=zhMOqUDsKew)")
                               
                                
                                st.write(
                                    """
                                    Below 10 workouts will help you to reduce Diabates.
                                    """
                            )
                                
                                st.write("[Watch the video >](https://www.youtube.com/watch?v=-uK8a80vyeI)")
                            
                            with left_column:
                                st.image(image3)  
                                
                                
                    with st.container():
                            #st.write("---")
                            left_column, right_column = st.columns(2)
                            
                            with left_column:
                                st.subheader("Stop Smoking")
                                st.markdown(":no_smoking:")
                                st.write("##")
                                st.write(
                                    """
                                    Diabetes risk and smoking are closely related, especially heavy smoking. It has been demonstrated that quitting over time lowers this risk. 
                                  - Below video by WHO will help you to quite tabaco using
                                        """
                            )
                                st.write("[Watch the video >](https://www.youtube.com/watch?v=H-vG5xyrYsI)")
     
                            with right_column:
                                st.image(image2 ,width=500)          
                                
                    with st.container():
                            #st.write("---")
                            left_column, right_column = st.columns(2)
                            
                            with right_column:
                                st.subheader("Drink Water")
                                st.markdown(":potable_water:")
                                st.write("##")
                                st.write(
                                    """
                                     -By drinking water instead of sugary drinks, you may be able to better control your insulin and blood sugar levels, lowering your chance of developing diabetes.
                                        """
                            )
                       
                            
                            with left_column:
                                st.image(image5,width=500)  
                                
                                
                    with st.container():
                            #st.write("---")
                            left_column, right_column = st.columns(2)
                            
                            with left_column:
                                st.subheader("Optimize your vitamin D levels")
                                st.markdown(":tomato:")
                                st.write("##")
                                st.write(
                                    """
                                    Your vitamin D levels may be improved by eating foods high in the vitamin or by taking supplements, which may help lower your chance of developing diabetes.
                                    """
                            )
                                
     
                            with right_column:
                                st.image(image6 ,width=500)  
            
            
        except:
            st.sidebar.error('email or password wrong ')
        
                           
                    
if __name__ == '__main__':
    main()                   
                    