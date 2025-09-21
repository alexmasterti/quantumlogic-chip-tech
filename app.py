import streamlit as st
import requests
import json

st.title("QuantumLogic Chip Technology Demo")

api = st.text_input("API base URL", "http://127.0.0.1:8000")

st.header("Quantum Search Demo")
bits = st.slider("Number of Qubits", 2, 5, 3)
target = st.number_input("Target state (int)", min_value=0, max_value=(2**bits)-1, value=5)
if st.button("Run Quantum Search"):
    r = requests.post(f"{api}/score", json={"bits": bits, "target": int(target)})
    st.write(r.json())

st.header("Amplitude Estimation Demo")
shots = st.slider("Shots", 200, 5000, 2000, step=200)
if st.button("Estimate Amplitude"):
    r = requests.post(f"{api}/amplitude", json={"bits": bits, "target": int(target), "shots": int(shots)})
    st.write(r.json())

st.header("Secure Payload Demo")
payload = {"sensor":"qchip","ts":"2025-09-21T12:00:00Z","data":[1,0,1,0,1]}
if st.button("Protect and Restore Payload"):
    p = requests.post(f"{api}/protect", json={"payload": payload}).json()
    r = requests.post(f"{api}/restore", json={"ciphertext_hex": p["ciphertext_hex"]}).json()
    st.write("Protected:", p)
    st.write("Restored:", r)
