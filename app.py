from openai import OpenAI
import streamlit as st

# Define o título da aplicação Streamlit
st.set_page_config(page_title='My chatBot', page_icon=':robot_face:')
st.title("Andre's chatbot")

# Inicializa o cliente OpenAI com a chave da API fornecida pelo usuário
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Verifica se o modelo OpenAI está definido na sessão; caso contrário, define o modelo padrão
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Verifica se a lista de mensagens está na sessão; caso contrário, inicializa a lista
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens previamente enviadas na interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Lê a entrada do usuário usando um componente de entrada de chat
if prompt := st.chat_input("Pergunte alguma coisa"):
    # Adiciona a mensagem do usuário à lista de mensagens na sessão
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Exibe a mensagem do usuário na interface
    with st.chat_message("user"):
        st.markdown(prompt)

    # Inicializa o espaço reservado para a resposta do assistente
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Itera sobre as respostas do modelo OpenAI em modo de streaming
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            # Atualiza a resposta completa com a resposta atual do modelo
            full_response += (response.choices[0].delta.content or "")

            # Atualiza dinamicamente a interface com a resposta parcial
            message_placeholder.markdown(full_response + "▌")

        # Exibe a resposta completa na interface após o término do streaming
        message_placeholder.markdown(full_response)

    # Adiciona a resposta do assistente à lista de mensagens na sessão
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
