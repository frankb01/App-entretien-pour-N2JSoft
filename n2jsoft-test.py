import streamlit as st
from openai import OpenAI
from io import BytesIO

# --- CONFIGURATION N2JSOFT ---
st.set_page_config(page_title="Prep Entretien N2JSoft", page_icon="💼")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages_n2f" not in st.session_state:
    st.session_state.messages_n2f = [
        {
            "role": "system", 
            "content": """Tu es le Head of Customer Success chez N2JSoft (solution N2F). 
            Tu mènes un entretien pour un poste de CSM à Lyon.
            
            TON OBJECTIF : 
            Vérifier si le candidat peut gérer l'onboarding technique (paramétrage), le support N2 et la rétention de clients comptables/RH.
            
            CONTEXTE POSTE :
            - Produit : N2F (Notes de frais).
            - Défis : Interfaçage avec ERP (Sage, SAP), règles de gestion complexes (TVA, indemnités kilométriques).
            
            DÉROULEMENT :
            1. Présente-toi brièvement (Head of CSM chez N2JSoft).
            2. Pose une première question sur la motivation pour la Fintech/SaaS lyonnais.
            3. Enchaîne sur des mises en situation de paramétrage technique et de support client difficile.
            4. Analyse si le candidat mentionne l'interfaçage comptable ou la pédagogie.
            
            Après 5 questions, donne un feedback détaillé 'Points Forts' et 'Axes d'Amélioration' par rapport à la fiche de poste N2JSoft."""
        }
    ]

st.title("🚀 Simulation Entretien N2JSoft (N2F)")
st.caption("Préparez-vous au poste de Customer Success Manager - Lyon")

# --- AFFICHAGE CHAT ---
for msg in st.session_state.messages_n2f:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- INPUT UTILISATEUR ---
if prompt := st.chat_input("Répondez à l'interviewer..."):
    st.session_state.messages_n2f.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages_n2f
        )
        response_text = resp.choices[0].message.content
        st.markdown(response_text)
        st.session_state.messages_n2f.append({"role": "assistant", "content": response_text})
        
        # Optionnel : Audio pour l'immersion
        # response_audio = client.audio.speech.create(model="tts-1", voice="onyx", input=response_text)
        # st.audio(BytesIO(response_audio.content), format="audio/mp3")
