# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 17:56:35 2023

@author: mateu
"""
import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import expon, weibull_min, kstest

# Define a função que ajusta as distribuições e realiza o teste de Kolmogorov-Smirnov
def fit_distribution(tempo_de_vida):
    # Ajusta a distribuição exponencial aos dados
    p_exp = expon.fit(tempo_de_vida)

    # Ajusta a distribuição Weibull aos dados
    p_weib = weibull_min.fit(tempo_de_vida)

    # Calcula o resultado do teste de Kolmogorov-Smirnov para ambas as distribuições
    ks_exp = kstest(tempo_de_vida, expon.cdf, args=p_exp)
    ks_weib = kstest(tempo_de_vida, weibull_min.cdf, args=p_weib)

    # Retorna o resultado do teste
    return ks_exp, ks_weib

# Define o app Streamlit
def app():
    # Define a página principal
    st.title("Teste de distribuição de falhas de equipamentos")

    # Elicita os dados de falhas de equipamentos
    n = st.number_input("Digite o número de equipamentos falhos:", min_value=1, value=1, step=1)
    tempo_de_vida = []
    for i in range(n):
        tempo_de_vida.append(float(st.text_input(f"Digite o tempo de vida (em horas) do equipamento {i+1}:", value="0.0")))

    # Realiza o ajuste das distribuições e o teste de Kolmogorov-Smirnov
    ks_exp, ks_weib = fit_distribution(tempo_de_vida)

    # Imprime os resultados
    st.write("Resultado do teste de Kolmogorov-Smirnov:")
    st.write("Distribuição exponencial - Estatística D:", ks_exp.statistic, "p-value:", ks_exp.pvalue)
    st.write("Distribuição Weibull - Estatística D:", ks_weib.statistic, "p-value:", ks_weib.pvalue)
    if ks_exp.pvalue > ks_weib.pvalue:
        st.write("A distribuição exponencial é a melhor escolha.")
    else:
        st.write("A distribuição Weibull é a melhor escolha.")

# Executa o app
if __name__ == '__main__':
    app()
