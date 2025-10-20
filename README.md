<p align="center">
    <img loading="lazy" src="https://files.engaged.com.br/5db0810e95b4f900077e887e/account/5db0810e95b4f900077e887e/xMCS8NFKTMqwhefy8WLd_catolica-horizontal.png" width="300">
</p>

# Comparativo entre Backtracking e Branch and Bound (B&B)
Projeto da disciplina de **Algoritmos Avançados**.

## Situação do Projeto
![Status](https://img.shields.io/badge/Status-Finalizado-green)

![Etapa](https://img.shields.io/badge/Etapa-N2-green)

## Introdução

Este projeto implementa e compara duas abordagens clássicas para o **problema da Soma de Subconjuntos (Subset Sum)**:

- **Backtracking puro**: percorre todas as combinações possíveis, realizando podas simples apenas quando a soma parcial ultrapassa o valor-alvo (*overflow*).
- **Branch and Bound (B&B)**: utiliza as mesmas bases do backtracking, mas adiciona **podas mais inteligentes**, como:
  - **Poda por overflow**: interrompe o ramo quando a soma ultrapassa o alvo;
  - **Poda por inviabilidade**: elimina ramos que, mesmo somando todos os valores restantes, não conseguem atingir o alvo;
  - **Ordenação decrescente dos elementos**: ajuda a testar primeiro os caminhos mais promissores.

A execução gera dados comparativos de desempenho entre as duas técnicas, mostrando:
- Tempo médio de execução;
- Nós explorados;
- Número de podas realizadas.

Também são gerados **gráficos** e um **arquivo CSV** com os resultados, permitindo análise visual e estatística do comportamento dos algoritmos conforme o tamanho do problema aumenta.

## Como executar

### Replit
1. Crie um projeto Python.
2. Envie `main.py`.
3. Clique em **Run** (ou execute `python3 main.py` no console).

### VSCode / Terminal
```bash
python main.py
```

## Contribuidores
A equipe envolvida nesta atividade é constituída por alunos da 7ª Fase (20252) do curso de Engenharia de Software do Centro Universitário Católica SC de Jaraguá do Sul.

<div align="center">
<table>
  <tr>
    <td align="center"><a href="https://github.com/HigorAz"><img loading="lazy" src="https://avatars.githubusercontent.com/u/141787745?v=4" width="115"><br><sub>Higor Azevedo</sub></a></td>
    <td align="center"><a href="https://github.com/AoiteFoca"><img loading="lazy" src="https://avatars.githubusercontent.com/u/141975272?v=4" width="115"><br><sub>Nathan Cielusinski</sub></a></td>
    <td align="center"><a href="https://github.com/MrNicolass"><img loading="lazy" src="https://avatars.githubusercontent.com/u/80847876?v=4" width="115"><br><sub>Nicolas Gustavo 
  </tr>
</div>
