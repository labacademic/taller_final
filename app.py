# app.py
# Streamlit minimal: usa el modelo para riesgo; si NO es alto, muestra cronograma.

import streamlit as st
from utils_local import MODEL, prob_riesgo, banda_riesgo, cronograma_frances, cuota_frances, TASA_MENSUAL

st.set_page_config(page_title="Riesgo de Crédito", page_icon="💳")
st.title("💳 Evaluación de credito")

st.caption("El modelo calcula la probabilidad. Si el riesgo NO es Alto, mostramos el cronograma.")
st.markdown("[🌐 Visita nuestra página web](https://www.labdatosperu.org/capacitaciones/machine-learning-con-python)")
st.markdown("[🎥 Enlace a la grabación del taller](https://us06web.zoom.us/clips/share/CnncGQ2ZQwGupnyiQ2_44g)")

# Entradas
salario = st.number_input("💼 Salario mensual (S/.)", min_value=0.0, value=2500.0, step=500.0)
monto   = st.number_input("💵 Monto del préstamo (S/.)", min_value=0.0, value=1200.0, step=100.0)
plazo  = st.number_input("📅 Número de cuotas (plazo en meses)", min_value=1, value=6, step=1)

if st.button("Calcular"):
    # 1) Probabilidad y banda con el modelo (incluye 'plazo')
    p = prob_riesgo(MODEL, salario=salario, monto=monto, plazo=plazo)
    b = banda_riesgo(p)

    # 2) Mostrar métricas
    cuota = cuota_frances(monto, plazo, TASA_MENSUAL)
    c1, c2, c3 = st.columns(3)
    c1.metric("Prob. mal pagador (modelo)", f"{p*100:.2f}%")
    c2.metric("Banda de riesgo", b)
    c3.metric("Tasa mensual fija", f"{TASA_MENSUAL*100:.2f}%")

    # 3) Cronograma si NO es alto
    if b == "Alto":
        st.warning("⚠️ Riesgo **Alto**: no se muestra el cronograma.")
    else:
        st.subheader("📄 Cronograma")
        st.caption(f"Cuota estimada: S/. {cuota:,.2f}")
        df = cronograma_frances(monto=monto, n_cuotas=plazo, tasa=TASA_MENSUAL)
        st.dataframe(df, use_container_width=True)




