# 1. Importação das bibliotecas necessárias
import pandas as pd
import statsmodels.api as sm
import numpy as np
import io

# 2. Preparação dos Dados
# Como não tenho acesso direto ao arquivo, eu recrio um conjunto de dados 
# com a mesma estrutura que a sua para demonstrar a análise.
# Em um cenário real, você carregaria seu arquivo CSV diretamente.
np.random.seed(42)
n_samples = 1000
df = pd.DataFrame({
    'unidade': np.random.choice(['Unidade A', 'Unidade B', 'Unidade C', 'Unidade D', 'Unidade E'], n_samples),
    'tipo_exame': np.random.choice(['sangue', 'urina', 'imagem', 'genético', 'covid', 'hormonal', 'alergia', np.nan], n_samples, p=[0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.05, 0.05]),
    'turno_mais_movimentado': np.random.choice(['manhã', 'tarde', 'noite'], n_samples),
    'temp_medio_exame': np.random.uniform(10, 30, n_samples),
    'tempo_entrega_resultado': np.random.uniform(1, 12, n_samples),
    'protocolo_emergencia': np.random.choice([True, False, np.nan], n_samples, p=[0.3, 0.6, 0.1]),
    'pacientes_dia': np.random.randint(20, 100, n_samples),
    'exames_realizados': np.random.randint(30, 100, n_samples),
    'quantidade_refrigeradores': np.random.randint(1, 5, n_samples),
    'tipo_refrigeracao': np.random.choice(['gaveta', 'vertical'], n_samples),
    'alinhamento_refrigeradores': np.random.choice(['lado_a_lado', 'em_L', 'dispersos'], n_samples),
    'direcao_centrifuga': np.random.choice(['leste', 'oeste', 'norte', 'sul'], n_samples)
})
# Adiciona valores nulos em 'temp_medio_exame' para simular o dataset real
df.loc[df.sample(frac=0.08).index, 'temp_medio_exame'] = np.nan

# 3. Engenharia e Limpeza de Features
# Criação da variável alvo: 1 para sucesso (no prazo), 0 para falha (fora do prazo)
df['laudo_no_prazo'] = (df['tempo_entrega_resultado'] <= 6).astype(int)

# Tratamento de valores nulos
# Para variáveis categóricas, preenchemos com a moda (valor mais frequente)
for col in ['tipo_exame', 'protocolo_emergencia']:
    mode_val = df[col].mode()[0]
    df[col] = df[col].fillna(mode_val)

# Para a variável numérica, preenchemos com a mediana
median_val = df['temp_medio_exame'].median()
df['temp_medio_exame'] = df['temp_medio_exame'].fillna(median_val)

# 4. Seleção de Variáveis para o Modelo
# Definimos as variáveis independentes (preditoras) que farão parte do modelo
features = [
    'pacientes_dia', 'exames_realizados', 'temp_medio_exame', 'protocolo_emergencia',
    'quantidade_refrigeradores', 'tipo_exame', 'turno_mais_movimentado', 'unidade',
    'tipo_refrigeracao', 'alinhamento_refrigeradores', 'direcao_centrifuga'
]
X = df[features].copy() # Usamos .copy() para evitar avisos de SettingWithCopyWarning
y = df['laudo_no_prazo']

# Convertemos a coluna booleana para numérica (0 ou 1)
X['protocolo_emergencia'] = X['protocolo_emergencia'].astype(int)

# Convertemos as variáveis categóricas em variáveis dummy (one-hot encoding)
# O `drop_first=True` remove a primeira categoria de cada variável para evitar multicolinearidade
# O `dtype=int` garante que as novas colunas sejam numéricas
X = pd.get_dummies(X, drop_first=True, dtype=int)

# Adicionamos uma constante (intercepto) ao modelo, o que é necessário para o statsmodels
X = sm.add_constant(X)

# 5. Construção e Treinamento do Modelo de Regressão Logística
# Criamos o modelo logístico
logit_model = sm.Logit(y, X)

# Treinamos o modelo com os dados
result = logit_model.fit()

# 6. Análise de Odds Ratio
# Extraímos os coeficientes (parâmetros) do modelo treinado
params = result.params
# Calculamos o intervalo de confiança para os coeficientes
conf = result.conf_int()
# Adicionamos os coeficientes ao dataframe do intervalo de confiança
conf['Odds Ratio'] = params
conf.columns = ['2.5%', '97.5%', 'Odds Ratio']

# Convertemos os coeficientes em Odds Ratio aplicando a função exponencial
# O Odds Ratio nos diz o quanto a chance de sucesso muda com o aumento de uma unidade no preditor
conf = np.exp(conf)

# Filtramos apenas as variáveis que são estatisticamente significativas (p-valor < 0.05)
significant_vars = result.pvalues[result.pvalues < 0.05].index
significant_odds_ratios = conf.loc[significant_vars]

# Ordenamos os resultados pelo valor do Odds Ratio para facilitar a interpretação
significant_odds_ratios = significant_odds_ratios.sort_values(by='Odds Ratio', ascending=False)

# 7. Exibição dos Resultados
# Separamos os fatores que aumentam a chance (OR > 1) dos que diminuem (OR < 1)
increasing_factors = significant_odds_ratios[significant_odds_ratios['Odds Ratio'] > 1]
decreasing_factors = significant_odds_ratios[significant_odds_ratios['Odds Ratio'] < 1]

print("Fatores Significativos que AUMENTAM a chance de entrega no prazo:")
print(increasing_factors)
print("\nFatores Significativos que DIMINUEM a chance de entrega no prazo:")
print(decreasing_factors)

# Para uma visão completa, você também pode imprimir o sumário do modelo
# print(result.summary())