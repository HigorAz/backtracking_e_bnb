import time, random, csv, os, json
from time import perf_counter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ============================
# CONFIGURAÇÕES GERAIS
# ============================
OUTPUT_DIR = "resultados_backtracking_bnb"
os.makedirs(OUTPUT_DIR, exist_ok=True)
random.seed(42)

# ============================
# PARTE 1 - BACKTRACKING PURO
# ============================
def subset_sum_backtracking(S, target):
    n = len(S)
    solution = []
    found = False
    nodes = 0
    prunings_overflow = 0

    def bt(index, current_sum, chosen):
        nonlocal found, solution, nodes, prunings_overflow
        nodes += 1

        # Solução encontrada
        if current_sum == target:
            solution = chosen.copy()
            found = True
            return True
       
        # Poda 1: soma ultrapassa o alvo
        if current_sum > target:
            prunings_overflow += 1
            return False

        # Fim da lista
        if index == n:
            return False

                # Tenta incluir S[index]
        if bt(index + 1, current_sum + S[index], chosen + [S[index]]):
            return True

        # Tenta excluir S[index]
        if bt(index + 1, current_sum, chosen):
            return True
        return False
    
    start = perf_counter()
    bt(0, 0, [])
    end = perf_counter()
    stats = {
        "tempo_s": end - start,
        "nodes_explorados": nodes,
        "prunings": prunings_overflow
    }
    return found, solution, stats

# ==================================
# PARTE 2 - BRANCH AND BOUND (PODAS)
# ==================================
def subset_sum_branch_and_bound(S, target):
    # Ordena os elementos em ordem decrescente (melhor poda)
    S = sorted(S, reverse=True)
    n = len(S)
    solution = []
    found = False
    nodes = 0
    prunings_overflow = 0
    prunings_inviavel = 0

    # Soma restante possível
    def remaining_sum(i):
        return sum(S[i:])

    def bb(index, current_sum, chosen):
        nonlocal found, solution, nodes, prunings_overflow, prunings_inviavel
        nodes += 1

        # Solução encontrada
        if current_sum == target:
            solution = chosen.copy()
            found = True
            return True

        if index == n:
            return False

        # Poda 1: soma passou do alvo
        if current_sum > target:
            prunings_overflow += 1
            return False

        # Poda 2: mesmo somando o restante, não atinge o alvo
        if current_sum + remaining_sum(index) < target:
            prunings_inviavel += 1
            return False

        # Inclui S[index]
        if bb(index + 1, current_sum + S[index], chosen + [S[index]]):
            return True

        # Exclui S[index]
        if bb(index + 1, current_sum, chosen):
            return True
        return False

    start = perf_counter()
    bb(0, 0, [])
    end = perf_counter()

    stats = {
        "tempo_s": end - start,
        "nodes_explorados": nodes,
        "prunings_overflow": prunings_overflow,
        "prunings_inviavel": prunings_inviavel
    }
    return found, solution, stats

# ==============================
# EXPERIMENTOS COMPARATIVOS
# ==============================
def executar_experimentos():
    base_large = [random.randint(1, 12) for _ in range(20)]
    random.shuffle(base_large)
    ns = [6, 8, 10, 12, 14, 16, 18]
    trials = 5
    resultados = []

    print("\nIniciando experimentos comparativos...\n")

    for n in ns:
        tempos_bt, tempos_bb = [], []
        nodes_bt, nodes_bb = [], []
        prunes_bt, prunes_bb = [], []
        prunes_inv = []

        for _ in range(trials):
            S = base_large[:n]
            target = sum(random.sample(S, k=max(1, n // 3)))

            # BACKTRACKING
            found_bt, sol_bt, stats_bt = subset_sum_backtracking(S, target)
            tempos_bt.append(stats_bt["tempo_s"])
            nodes_bt.append(stats_bt["nodes_explorados"])
            prunes_bt.append(stats_bt["prunings"])

            # BRANCH AND BOUND
            found_bb, sol_bb, stats_bb = subset_sum_branch_and_bound(S, target)
            tempos_bb.append(stats_bb["tempo_s"])
            nodes_bb.append(stats_bb["nodes_explorados"])
            prunes_bb.append(stats_bb["prunings_overflow"] + stats_bb["prunings_inviavel"])
            prunes_inv.append(stats_bb["prunings_inviavel"])

        resultados.append({
            "n": n,
            "tempo_bt": np.mean(tempos_bt),
            "tempo_bb": np.mean(tempos_bb),
            "nodes_bt": int(np.mean(nodes_bt)),
            "nodes_bb": int(np.mean(nodes_bb)),
            "podas_bt": int(np.mean(prunes_bt)),
            "podas_bb": int(np.mean(prunes_bb)),
            "podas_inviaveis_bb": int(np.mean(prunes_inv))
        })
        print(f"n={n}: tempo_BT={np.mean(tempos_bt):.6f}s, tempo_BB={np.mean(tempos_bb):.6f}s, "
              f"nodes_BT={int(np.mean(nodes_bt))}, nodes_BB={int(np.mean(nodes_bb))}")
    return resultados

# ==============================
# GERAÇÃO DE GRÁFICOS E CSV
# ==============================
def salvar_resultados(resultados):
    csv_path = os.path.join(OUTPUT_DIR, "resultados_comparativos.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "tempo_bt", "tempo_bb", "nodes_bt", "nodes_bb", "podas_bt", "podas_bb"])
        for r in resultados:
            writer.writerow([r["n"], r["tempo_bt"], r["tempo_bb"], r["nodes_bt"], r["nodes_bb"], r["podas_bt"], r["podas_bb"]])
    print(f"\nResultados salvos em: {csv_path}")

    n_vals = [r["n"] for r in resultados]

    # --- Tempo médio ---
    plt.figure(figsize=(8,5))
    plt.plot(n_vals, [r["tempo_bt"] for r in resultados], marker='o', label='Backtracking')
    plt.plot(n_vals, [r["tempo_bb"] for r in resultados], marker='o', label='Branch and Bound')
    plt.xlabel("Tamanho n")
    plt.ylabel("Tempo médio (s)")
    plt.title("Tempo médio de execução")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "tempo_comparativo.png"))
    plt.close()

    # --- Nodes explorados ---
    plt.figure(figsize=(8,5))
    plt.plot(n_vals, [r["nodes_bt"] for r in resultados], marker='o', label='Backtracking')
    plt.plot(n_vals, [r["nodes_bb"] for r in resultados], marker='o', label='Branch and Bound')
    plt.xlabel("Tamanho n")
    plt.ylabel("Nós explorados (média)")
    plt.title("Comparativo de nós explorados")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "nodes_comparativo.png"))
    plt.close()

    # --- Podas ---
    plt.figure(figsize=(8,5))
    plt.plot(n_vals, [r["podas_bt"] for r in resultados], marker='o', label='Backtracking')
    plt.plot(n_vals, [r["podas_bb"] for r in resultados], marker='o', label='Branch and Bound')
    plt.xlabel("Tamanho n")
    plt.ylabel("Número médio de podas")
    plt.title("Comparativo de podas")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "podas_comparativo.png"))
    plt.close()
    print("Gráficos comparativos gerados com sucesso!")
    return csv_path


# ==============================
# EXECUÇÃO PRINCIPAL
# ==============================
if __name__ == "__main__":
    resultados = executar_experimentos()
    df = pd.DataFrame(resultados)
    print("\nResumo Final:")
    print(df.to_string(index=False))
    salvar_resultados(resultados)