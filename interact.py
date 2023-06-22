import requests
import streamlit as st 
from streamlit_chat import message 

#Inputs 
token = st.secrets["api_secret"]
bot_link = st.secrets["bot_link"]

header = {
    # 'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    # Already added when you pass json=
    # 'Content-Type': 'application/json',
    'accept': 'application/json',
    'token': token,
}

#prompting function

def generate_response(prompt, bot, load):
    json_data = {
    'question': prompt,
    }
    response = requests.post(bot, headers=load, json=json_data)
    clean_response= response.json()[0]
    return clean_response["data"]["answer"]

st.title("climabot: Streamlit + Writesonic")

if 'generated' not in st.session_state:
    st.session_state["generated"] = []

# st.session_state.generated = []

# print(st.session_state.generated)


# print(st.session_state['generated'])

if 'past' not in st.session_state:
    st.session_state['past'] = []
# st.write(st.session_state.past)


# print('generated' not in st.session_state)

def get_text():
    input_text = st.text_input("You: ","Hello Writesonic", key="input")
    return input_text 

user_input = get_text()

if user_input:
    output = generate_response(user_input, bot_link, header)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)
    
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], logo= "https://media.licdn.com/dms/image/C560BAQGG5VG3rcnNMA/company-logo_200_200/0/1568920482000?e=2147483647&v=beta&t=hmeNuvbdLJeC3Rif6X8xc1SFY-gN-Ia5tiRVuSU2vhQ", key=str(i))
        message(st.session_state['past'][i], avatar_style="adventurer", is_user=True, key=str(i) + '_user')
