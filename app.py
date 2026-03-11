import pandas as pd
import scipy.stats
import streamlit as st
import time

if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

st.header('Lanzar una moneda')

chart_placeholder = st.empty()

def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    outcome_no = 0
    outcome_1_count = 0
    data = {'media': [0.5], 'referencia': [0.5]}
    df_chart = pd.DataFrame(data)

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        nueva_fila = pd.DataFrame({'media': [mean], 'referencia': [0.5]})
        df_chart = pd.concat([df_chart, nueva_fila], ignore_index=True)
        chart_placeholder.line_chart(
            df_chart,
            y=['media', 'referencia'],
            y_label='Probabilidad',
            x_label='Lanzamientos',
            color=['#FF4B4B', '#444444']
        )
        time.sleep(0.05)

    return mean

number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                     columns=['no', 'iteraciones', 'media'])
        ],
        axis=0)
    st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].reset_index(drop=True)

st.write(st.session_state['df_experiment_results'])