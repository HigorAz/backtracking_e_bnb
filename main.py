# -*- coding: utf-8 -*-
"""
Comparativo Backtracking vs Branch and Bound
Caso fixo: S={3,5,7,2,8,6,4,1,9,10}, T=15
Visualização aprimorada com gráficos comparativos e anotações.
"""

import os, csv, json
from time import perf_counter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ============================
# CONFIGURAÇÕES
# ============================
OUTPUT_DIR = "resultados_final_bnb_bt"
os.makedirs(OUTPUT_DIR, exist_ok=True)

S_FIXED = [3,5,7,2,8,6,4,1,9,10]
T_FIXED = 15

# ============================
# PARTE 1 - BACKTRACKING
# ============================
def subset_sum_backtracking(S, target):
    n = len(S)
    solution = []
    found = False
    nodes = 0
    podas = 0
    logs_poda = []

    def bt(index, current_sum, chosen):
        nonlocal found, solution, nodes, podas
        nodes += 1

        # Solução encontrada
        if current_sum == target:
            solution = chosen.copy()
            found = True
            return True
        
        # Poda: soma ultrapassa o alvo
        if current_sum > target:
            podas += 1
            logs_poda.append(f"Poda por overflow em index={index}, soma={current_sum}, caminho={chosen}")
            return False

        # Fim da lista
        if index == n:
            return False

        # Incluir
        if bt(index + 1, current_sum + S[index], chosen + [S[index]]):
            return True

        # Excluir
        if bt(index + 1, current_sum, chosen):
            return True

        return False

    start = perf_counter()
    bt(0, 0, [])
    end = perf_counter()

    stats = {
        "tempo_s": end - start,
        "nodes": nodes,
        "podas": podas,
        "logs": logs_poda
    }
    return found, solution, stats


# ============================
# PARTE 2 - BRANCH AND BOUND
# ============================
def subset_sum_branch_and_bound(S, target):
    S = sorted(S, reverse=True)
    n = len(S)
    solution = []
    found = False
    nodes = 0
    podas_overflow = 0
    podas_inviavel = 0
    logs_poda = []

    suffix_sum = [0]*(n+1)
    for i in range(n-1, -1, -1):
        suffix_sum[i] = suffix_sum[i+1] + S[i]

    def bb(index, current_sum, chosen):
        nonlocal found, solution, nodes, podas_overflow, podas_inviavel
        nodes += 1

        if current_sum == target:
            solution = chosen.copy()
            found = True
            return True

        if index == n:
            return False

        # Poda 1: soma passou do alvo
        if current_sum > target:
            podas_overflow += 1
            logs_poda.append(f"Poda overflow em index={index}, soma={current_sum}, caminho={chosen}")
            return False

        # Poda 2: mesmo somando tudo não alcança o alvo
        if current_sum + suffix_sum[index] < target:
            podas_inviavel += 1
            logs_poda.append(f"Poda inviável em index={index}, soma={current_sum}, caminho={chosen}")
            return False

        # Incluir
        if bb(index + 1, current_sum + S[index], chosen + [S[index]]):
            return True

        # Excluir
        if bb(index + 1, current_sum, chosen):
            return True

        return False

    start = perf_counter()
    bb(0, 0, [])
    end = perf_counter()

    stats = {
        "tempo_s": end - start,
        "nodes": nodes,
        "podas_overflow": podas_overflow,
        "podas_inviavel": podas_inviavel,
        "logs": logs_poda
    }
    return found, solution, stats


# ============================
# EXECUÇÃO E COLETA DE RESULTADOS
# ============================
def executar():
    print("Executando caso fixo: S={}, T={}".format(S_FIXED, T_FIXED))

    found_bt, sol_bt, st_bt = subset_sum_backtracking(S_FIXED, T_FIXED)
    found_bb, sol_bb, st_bb = subset_sum_branch_and_bound(S_FIXED, T_FIXED)

    resultados = pd.DataFrame([
        {
            "Algoritmo": "Backtracking",
            "Tempo (s)": st_bt["tempo_s"],
            "Nós explorados": st_bt["nodes"],
            "Podas (overflow)": st_bt["podas"],
            "Podas (inviáveis)": 0,
            "Solução": str(sol_bt)
        },
        {
            "Algoritmo": "Branch and Bound",
            "Tempo (s)": st_bb["tempo_s"],
            "Nós explorados": st_bb["nodes"],
            "Podas (overflow)": st_bb["podas_overflow"],
            "Podas (inviáveis)": st_bb["podas_inviavel"],
            "Solução": str(sol_bb)
        }
    ])

    print("\nResumo comparativo:\n", resultados)

    # Salvar CSV e logs
    resultados.to_csv(os.path.join(OUTPUT_DIR, "comparativo_resultados.csv"), index=False, encoding="utf-8")
    with open(os.path.join(OUTPUT_DIR, "logs_backtracking.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(st_bt["logs"]))
    with open(os.path.join(OUTPUT_DIR, "logs_branch_bound.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(st_bb["logs"]))

    # ============================
    # GRÁFICOS COM VISUALIZAÇÃO MELHORADA
    # ============================
    plt.style.use("seaborn-v0_8-colorblind")

    # 1) TEMPO
    fig, ax = plt.subplots(figsize=(8,5))
    bars = ax.bar(resultados["Algoritmo"], resultados["Tempo (s)"], color=["#377eb8", "#4daf4a"], alpha=0.8)
    ax.set_title("Tempo de execução (s)", fontsize=14, weight="bold")
    ax.set_ylabel("Tempo (segundos)")
    ax.bar_label(bars, fmt="%.6f", padding=3, fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "grafico_tempo.png"), dpi=300)
    plt.close()

    # 2) NÓS
    fig, ax = plt.subplots(figsize=(8,5))
    bars = ax.bar(resultados["Algoritmo"], resultados["Nós explorados"], color=["#ff7f00", "#984ea3"], alpha=0.8)
    ax.set_title("Nós explorados", fontsize=14, weight="bold")
    ax.set_ylabel("Quantidade de nós")
    ax.bar_label(bars, fmt="%d", padding=3, fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "grafico_nos.png"), dpi=300)
    plt.close()

    # 3) PODAS AGRUPADAS
    fig, ax = plt.subplots(figsize=(9,5))
    labels = ["Overflow", "Inviável"]
    bt_podas = [st_bt["podas"], 0]
    bb_podas = [st_bb["podas_overflow"], st_bb["podas_inviavel"]]
    x = np.arange(len(labels))
    width = 0.35

    bars1 = ax.bar(x - width/2, bt_podas, width, label="Backtracking", color="#e41a1c", alpha=0.8)
    bars2 = ax.bar(x + width/2, bb_podas, width, label="Branch and Bound", color="#377eb8", alpha=0.8)

    ax.set_title("Comparativo de podas por tipo", fontsize=14, weight="bold")
    ax.set_ylabel("Quantidade")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.bar_label(bars1, fmt="%d", padding=3)
    ax.bar_label(bars2, fmt="%d", padding=3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "grafico_podas.png"), dpi=300)
    plt.close()

    print("\nGráficos salvos em:", os.path.abspath(OUTPUT_DIR))
    print(" - grafico_tempo.png")
    print(" - grafico_nos.png")
    print(" - grafico_podas.png")

if __name__ == "__main__":
    executar()
