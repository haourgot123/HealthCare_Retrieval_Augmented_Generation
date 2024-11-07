import streamlit as st
from chatbot import ChatbotAssistant

if 'llm' not in st.session_state:
    st.session_state.llm = ChatbotAssistant()

st.title('🤖 HealthCare Chatbot')

if 'messages' not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    if st.button('🎯 New chat', use_container_width=True):
        st.session_state.messages = []

if len(st.session_state.messages) == 0:
    with st.chat_message('assistant'):
        st.markdown('🙋‍♂️ Xin chào ! Tôi có thể giúp gì cho bạn.')

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input('Hãy nhập câu hỏi của bạn'):
    st.session_state.messages.append(
        {
            'role': 'user',
            'content': prompt
        }
    )
    with st.chat_message('user'):
        st.markdown(prompt)
    with st.chat_message('assistant'):
        full_res = ''
        holder = st.empty()
        for response in st.session_state.llm.invoke(
            query = prompt
        ):
            full_res += (response or "")
            holder.markdown(full_res + '|')
            holder.markdown(full_res)
        holder.markdown(full_res)
    st.session_state.messages.append(
        {
            'role' : 'assistant',
            'content': full_res
        }
    )



            
        