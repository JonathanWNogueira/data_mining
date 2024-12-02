## Análise das Regras de Associação - Apriori

### Regras com Maior Suporte

As regras com maior suporte indicam as combinações de antecedentes e consequentes que ocorreram com maior frequência no conjunto de dados. Abaixo estão as regras com maior suporte:

| Antecedente                                             | Consequente  | Suporte | Confiança | Lift  |
|---------------------------------------------------------|--------------|---------|-----------|-------|
| Bacharelado em Sistemas de Informação - C380148200685    | Aprovado     | 0.01651 | 0.31579   | 1.143 |
| Ciência da Computação - Bacharelado - C380148200685     | Aprovado     | 0.01303 | 0.40000   | 1.448 |
| Bacharelado em Sistemas de Informação - C380148200685    | Reprovado    | 0.01651 | 0.31579   | 1.143 |
| Ciência da Computação - Bacharelado - C380148200685     | Reprovado    | 0.01303 | 0.33333   | 1.207 |
| Bacharelado em Sistemas de Informação - E978402380148    | Aprovado     | 0.01043 | 0.33333   | 1.207 |
| Bacharelado em Sistemas de Informação - I200380893402    | Aprovado     | 0.00782 | 0.44444   | 1.609 |
| Bacharelado em Sistemas de Informação - C200380893402    | Aprovado     | 0.00869 | 0.40000   | 1.448 |
| Bacharelado em Sistemas de Informação - C200380893402    | Reprovado    | 0.00869 | 0.40000   | 1.448 |
| Bacharelado em Sistemas de Informação - E681200461218    | Reprovado    | 0.00869 | 0.40000   | 1.448 |

Essas regras mostram quais cursos estão mais frequentemente associados aos resultados de aprovação ou reprovação. Por exemplo, o "Bacharelado em Sistemas de Informação - C380148200685" tem uma alta associação tanto com a aprovação quanto com a reprovação.

### Regras com Maior Confiança

As regras com maior confiança indicam a probabilidade de o consequente ocorrer, dado que o antecedente esteja presente. Abaixo estão as regras com maior confiança:

| Antecedente                                              | Consequente  | Suporte | Confiança | Lift  |
|----------------------------------------------------------|--------------|---------|-----------|-------|
| Engenharia Química - A292200218320                        | Reprovado    | 0.00174 | 0.66667   | 2.413 |
| Curso de Engenharia Aeroespacial - A292200218320          | Aprovado     | 0.00174 | 0.66667   | 2.413 |
| Engenharia Química - P380148200                           | Reprovado    | 0.00174 | 0.66667   | 2.413 |
| Ciência da Computação - Bacharelado - C888148218402       | Reprovado    | 0.00087 | 0.50000   | 1.810 |
| Ciência da Computação - Bacharelado - E200380461148       | Reprovado    | 0.00087 | 0.50000   | 1.810 |
| Química - Licenciatura - B200380461148                    | Aprovado     | 0.00087 | 0.50000   | 1.810 |
| Engenharia Elétrica - B512402380642                       | Reprovado    | 0.00087 | 0.50000   | 1.810 |
| Química Industrial - P512200642                           | Reprovado    | 0.00087 | 0.50000   | 1.810 |
| Ciência da Computação - Bacharelado - E200380461148       | Aprovado     | 0.00087 | 0.50000   | 1.810 |
| Curso de Engenharia Aeroespacial - B200380461148          | Reprovado    | 0.00174 | 0.50000   | 1.810 |
| Engenharia Elétrica - B512402380642                       | Aprovado     | 0.00087 | 0.50000   | 1.810 |
| Engenharia Elétrica - B888642512642                       | Reprovado    | 0.00174 | 0.50000   | 1.810 |
| Bacharelado em Sistemas de Informação - C402380642148     | Reprovado    | 0.00087 | 0.50000   | 1.810 |

Essas regras destacam cursos específicos com alta confiança associada a aprovação ou reprovação. Por exemplo, a regra associando "Engenharia Química - A292200218320" com "Reprovado" tem uma confiança de 66,67%, o que significa que a probabilidade de reprovação é muito alta quando esse curso está presente.

#### Análises Detalhadas das Regras com Maior Confiança

- **Engenharia Química - A292200218320 → Reprovado (Confiança: 0.6667):**
  A alta confiança aqui sugere que, para os alunos desse curso específico, há uma probabilidade considerável de reprovação. Isso pode ser usado para investigar se há fatores específicos dentro desse curso que influenciam a taxa de reprovação, como dificuldade, currículo ou carga de trabalho.

- **Curso de Engenharia Aeroespacial - A292200218320 → Aprovado (Confiança: 0.6667):**
  Curiosamente, um outro curso, com o mesmo professor, mas com uma confiança alta para aprovação. Isso poderia indicar que os alunos desse curso têm uma boa taxa de aprovação, o que pode ser interessante para destacar pontos positivos sobre o curso, como boa orientação ou preparação. Além disso, por ser com o mesmo professor, poderia ser analisada a possibilidade de que este professor favorece alunos do curso de Engenharia Aeroespacial, e desfavorece os alunos de Engenharia Química. Entretanto, não podemos afirmar isso apenas com estes dados analisados, visto que somente a taxa de reprovação e aprovação deste professor com os alunos dos cursos não prova isso. Além disso, não são numerosos o suficiente os casos analisados. Embora o suporte seja baixo, essas duas regras ainda são bastante interessantes e permitem a criação de hipóteses que podem ser investigadas.

- **Engenharia Química - P380148200 → Reprovado (Confiança: 0.6667):**
  Similar à primeira, isso reforça a ideia de que alunos do curso de Engenharia Química enfrentam uma taxa de reprovação considerável, o que pode exigir atenção para melhorar o desempenho dos alunos nesse curso.

Essas três regras apresentadas foram as que apresentaram maior confiança, e nos fornecem algumas informações inegavelmente interessantes.

### Conclusão

- **Maior Suporte:** Cursos como "Bacharelado em Sistemas de Informação - C380148200685" têm uma alta frequência de associação com aprovação e reprovação, o que sugere que esses cursos são comuns nas transações.
- **Maior Confiança:** Algumas regras indicam uma probabilidade bastante alta de ocorrência do consequente, como no caso de "Engenharia Química" e "Curso de Engenharia Aeroespacial" com alta confiança na reprovação ou aprovação.

Essas informações podem ser úteis para a análise do desempenho dos alunos em diferentes cursos e para identificar padrões em suas trajetórias acadêmicas.
