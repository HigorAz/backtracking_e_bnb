<p align="center">
    <img loading="lazy" src="https://files.engaged.com.br/5db0810e95b4f900077e887e/account/5db0810e95b4f900077e887e/xMCS8NFKTMqwhefy8WLd_catolica-horizontal.png" width="300">
</p>

# Comparativo entre Backtracking e Branch and Bound (B&B)
Projeto da disciplina de **Algoritmos Avançados**, com foco na análise de desempenho entre as técnicas de busca **Backtracking** e **Branch and Bound (B&B)**.

---

## Situação do Projeto
![Status](https://img.shields.io/badge/Status-Finalizado-green)
![Etapa](https://img.shields.io/badge/Etapa-N2-green)
![Linguagem](https://img.shields.io/badge/Linguagem-Python-blue)
![Bibliotecas](https://img.shields.io/badge/Libs-Matplotlib%20%7C%20NumPy%20%7C%20Pandas-lightgrey)

---

## Introdução

O projeto implementa e compara duas abordagens clássicas para o **problema da Soma de Subconjuntos (Subset Sum)**, utilizando uma **instância fixa**:
> S = {3, 5, 7, 2, 8, 6, 4, 1, 9, 10}, alvo (T) = 15.

O objetivo é identificar **qual subconjunto de S soma exatamente T**, medindo o desempenho de cada método.

### Métodos utilizados

#### **Backtracking Puro**
- Explora todas as combinações possíveis de forma recursiva.
- Utiliza uma única **poda**: interrompe o ramo quando a soma ultrapassa o valor-alvo (*overflow*).
- Garante a solução correta, mas apresenta alto custo computacional conforme o número de elementos cresce.

#### **Branch and Bound (B&B)**
- É uma versão otimizada do Backtracking, que aplica **podas adicionais** e uma **ordenação decrescente** dos elementos.
- Utiliza:
  - **Poda por overflow:** interrompe o ramo quando a soma parcial passa do alvo.
  - **Poda por inviabilidade:** evita percorrer caminhos que, mesmo somando todos os valores restantes, não alcançariam o alvo.
  - **Ordenação decrescente:** garante que os elementos maiores sejam testados primeiro, aumentando a chance de poda precoce.
- Essa técnica é amplamente usada em **problemas combinatórios de otimização**, como o *Subset Sum* e o *Knapsack Problem*.

---

## Estrutura do Código

O script principal (`main.py`) é dividido em três partes:

1. **Implementação dos algoritmos**:
   - `subset_sum_backtracking()` -> método de busca exaustiva com poda simples.
   - `subset_sum_branch_and_bound()` -> versão aprimorada com podas múltiplas e ordenação.
2. **Execução e coleta de resultados**:
   - Mede **tempo de execução**, **nós explorados** e **quantidade de podas**.
   - Armazena logs detalhados de cada poda detectada.
3. **Geração de relatórios e gráficos**:
   - Cria uma pasta `resultados_final_bnb_bt/` contendo:
     - `comparativo_resultados.csv` — resumo em formato tabular.
     - `logs_backtracking.txt` e `logs_branch_bound.txt` — registro das podas.
     - Gráficos em PNG com visualização comparativa.

---

## Gráficos e Visualização

O código gera automaticamente três gráficos comparativos usando **Matplotlib**:

### 1. Tempo de Execução (`grafico_tempo.png`)
Mostra o tempo total gasto por cada algoritmo.  
> O Branch and Bound apresenta tempo menor, comprovando sua eficiência nas podas.

### 2. Nós Explorados (`grafico_nos.png`)
Indica quantos nós foram visitados durante a execução.  
> O Backtracking tende a crescer exponencialmente, enquanto o Branch and Bound mantém crescimento controlado.

### 3. Comparativo de Podas (`grafico_podas.png`)
Compara o número de podas de cada tipo (*overflow* e *inviável*).  
> Demonstra que o Branch and Bound realiza mais cortes estratégicos, reduzindo o espaço de busca.

### Estrutura gerada
```
 resultados_final_bnb_bt/
 ┣ comparativo_resultados.csv
 ┣ logs_backtracking.txt
 ┣ logs_branch_bound.txt
 ┣ grafico_tempo.png
 ┣ grafico_nos.png
 ┗ grafico_podas.png
```

---

## Como Executar

### No Replit
1. Crie um novo projeto **Python**.
2. Envie o arquivo `main.py`.
3. Clique em **Run** ou execute no console:
   ```bash
   python3 main.py
   ```

### No VSCode ou Terminal
1. Instale as dependências:
   ```bash
   pip install matplotlib numpy pandas
   ```
2. Execute:
   ```bash
   python main.py
   ```

Os resultados e gráficos serão salvos automaticamente na pasta `resultados_final_bnb_bt`.

---

## Interpretação dos Resultados

- O **Backtracking** confirma a solução, mas gasta muito mais tempo e percorre praticamente toda a árvore de possibilidades.
- O **Branch and Bound** usa inteligência de poda: elimina ramos inviáveis logo no início e chega ao resultado com menos esforço.
- Assim como no artigo de *Guéret, Jussien e Prins (2000)*, os resultados mostram que **estratégias de poda reduzem drasticamente o número de retrocessos**.
- Em resumo: o Branch and Bound é o **Backtracking otimizado** — mais rápido, mais eficiente e igualmente correto.

---

## Contribuidores

A equipe envolvida nesta atividade é composta por alunos da 7ª Fase (20252) do curso de Engenharia de Software do **Centro Universitário Católica SC - Jaraguá do Sul**.

<div align="center">
<table>
  <tr>
    <td align="center"><a href="https://github.com/HigorAz"><img loading="lazy" src="https://avatars.githubusercontent.com/u/141787745?v=4" width="115"><br><sub>Higor Azevedo</sub></a></td>
    <td align="center"><a href="https://github.com/AoiteFoca"><img loading="lazy" src="https://avatars.githubusercontent.com/u/141975272?v=4" width="115"><br><sub>Nathan Cielusinski</sub></a></td>
    <td align="center"><a href="https://github.com/MrNicolass"><img loading="lazy" src="https://avatars.githubusercontent.com/u/80847876?v=4" width="115"><br><sub>Nicolas Gustavo</sub></a></td>
  </tr>
</table>
</div>
