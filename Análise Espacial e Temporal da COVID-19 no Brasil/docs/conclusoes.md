# Conclusões e próximos passos

## O que foi entregue

O projeto estruturou cinco perguntas analíticas em consultas independentes e reutilizáveis. A solução demonstra o uso de CTEs, funções de janela, médias móveis, rankings, junções territoriais e indicadores normalizados por população.

## O que os resultados permitem observar

- velocidade e ritmo de vacinação ao longo do tempo;
- diferenças de cobertura entre municípios e estados;
- disponibilidade de leitos em relação à população;
- municípios com maior pressão relativa entre casos graves e capacidade hospitalar;
- distribuição da vacinação por faixa etária.

## Limitações

As consultas não constituem um estudo causal. Os indicadores dependem da cobertura, da qualidade e da atualização das bases públicas. Comparações entre municípios devem considerar população, perfil etário, subnotificação, disponibilidade de leitos e diferenças na notificação.

## Evolução recomendada

A próxima versão deve implementar as views analíticas previstas, adicionar testes de qualidade e publicar uma camada visual com pelo menos: evolução temporal, mapa/ranking territorial, cobertura vacinal e pressão hospitalar.
