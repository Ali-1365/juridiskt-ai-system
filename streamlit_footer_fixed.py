
# Historik-sektion om det finns historik
if st.session_state.prompt_history:
    with st.expander("Tidigare frågor"):
        for i, previous_prompt in enumerate(st.session_state.prompt_history):
            if st.button(f"Använd igen: {previous_prompt[:50]}...", key=f"history_{i}"):
                st.session_state.prompt = previous_prompt
                st.rerun()

# Lägg till "Tillbaka till portalen"-länk längst ner 
st.markdown("---")
st.markdown("⬅️ [Tillbaka till AI-portalen](https://juridisk-ai-portal.alihabibpoor86.repl.co)")
