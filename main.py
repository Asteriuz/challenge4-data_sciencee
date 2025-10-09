import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Carregar dados
df = pd.read_csv('data/dasa-final.csv')

# Visualizar estrutura inicial dos dados
print("Dimensões do dataset:", df.shape)
print("\nPrimeiras linhas:")
print(df.head())
print("\nInformações sobre as colunas:")
print(df.info())
print("\nEstatísticas descritivas da variável target:")
print(df['tempo_entrega_resultado'].describe())

# ==========================
# PROBLEMA 2: EXAMES DE IMAGEM
# ==========================
print("\n" + "="*60)
print("PROBLEMA 2: ANÁLISE DE ATRASOS EM EXAMES DE IMAGEM")
print("="*60)

# Filtrar apenas exames de imagem
df_imagem = df[df['tipo_exame'] == 'imagem'].copy()
print(f"\nTotal de exames de imagem: {len(df_imagem)}")

# Criar variável binária: 1 se tempo > 36 horas, 0 caso contrário
df_imagem['atraso_36h'] = (df_imagem['tempo_entrega_resultado'] > 36).astype(int)
print(f"Taxa de atrasos > 36h: {df_imagem['atraso_36h'].mean():.2%}")

# Selecionar variáveis relevantes para análise
variaveis_numericas = ['pacientes_dia', 'exames_realizados', 'temp_medio_exame', 
                       'quantidade_refrigeradores', 'hora_inicio_turno', 'dia_fechamento']

variaveis_categoricas = ['unidade', 'mes', 'turno_mais_movimentado', 'protocolo_emergencia',
                         'direcao_centrifuga', 'alinhamento_refrigeradores', 
                         'cor_parede_laboratorio', 'cor_parede_coleta',
                         'aromatizador_eucalipto', 'cheiro_ambiente', 'musica_ambiente',
                         'cor_jaleco_funcionario', 'elemento_decorativo', 
                         'janela_virada_para', 'tipo_refrigeracao']

# Preparar dados para regressão
X_imagem = pd.get_dummies(df_imagem[variaveis_categoricas], drop_first=True)
X_imagem[variaveis_numericas] = df_imagem[variaveis_numericas]

# Remover valores nulos se houver
X_imagem = X_imagem.fillna(X_imagem.median())
y_imagem = df_imagem['atraso_36h']

# Padronizar variáveis numéricas
scaler = StandardScaler()
X_imagem[variaveis_numericas] = scaler.fit_transform(X_imagem[variaveis_numericas])

# Treinar modelo de regressão logística
log_reg_imagem = LogisticRegression(max_iter=1000, random_state=42)
log_reg_imagem.fit(X_imagem, y_imagem)

# Calcular odds ratios
coef_imagem = pd.DataFrame({
    'variavel': X_imagem.columns,
    'coeficiente': log_reg_imagem.coef_[0],
    'odds_ratio': np.exp(log_reg_imagem.coef_[0])
})
coef_imagem = coef_imagem.sort_values('odds_ratio', ascending=False)

print("\nTop 10 fatores que AUMENTAM o risco de atraso (Odds Ratio > 1):")
print(coef_imagem[coef_imagem['odds_ratio'] > 1].head(10)[['variavel', 'odds_ratio']])

print("\nTop 10 fatores que REDUZEM o risco de atraso (Odds Ratio < 1):")
print(coef_imagem[coef_imagem['odds_ratio'] < 1].head(10)[['variavel', 'odds_ratio']])

# Score do modelo
score_imagem = log_reg_imagem.score(X_imagem, y_imagem)
print(f"\nAcurácia do modelo: {score_imagem:.2%}")

# ==========================
# PROBLEMA 3: PAREDE LARANJA
# ==========================
print("\n" + "="*60)
print("PROBLEMA 3: ANÁLISE DO IMPACTO DA PAREDE LARANJA")
print("="*60)

# Usar todos os dados para esta análise
df_parede = df.copy()

# Criar variável binária para parede laranja na sala de coleta
df_parede['parede_laranja'] = (df_parede['cor_parede_coleta'] == 'laranja').astype(int)

# Estatísticas descritivas
print(f"\nTotal de observações com parede laranja: {df_parede['parede_laranja'].sum()}")
print(f"Proporção com parede laranja: {df_parede['parede_laranja'].mean():.2%}")

# Comparação de médias
tempo_com_laranja = df_parede[df_parede['parede_laranja'] == 1]['tempo_entrega_resultado']
tempo_sem_laranja = df_parede[df_parede['parede_laranja'] == 0]['tempo_entrega_resultado']

print(f"\nTempo médio COM parede laranja: {tempo_com_laranja.mean():.2f} horas")
print(f"Tempo médio SEM parede laranja: {tempo_sem_laranja.mean():.2f} horas")
print(f"Diferença: {tempo_com_laranja.mean() - tempo_sem_laranja.mean():.2f} horas")

# Criar variável binária para atraso (usando mediana como threshold)
mediana_tempo = df_parede['tempo_entrega_resultado'].median()
df_parede['atraso'] = (df_parede['tempo_entrega_resultado'] > mediana_tempo).astype(int)
print(f"\nMediana do tempo de entrega: {mediana_tempo:.2f} horas")

# Preparar dados incluindo variáveis de controle
variaveis_controle = ['tipo_exame', 'pacientes_dia', 'exames_realizados', 
                      'temp_medio_exame', 'protocolo_emergencia', 
                      'turno_mais_movimentado', 'tipo_refrigeracao']

X_parede = pd.get_dummies(df_parede[['parede_laranja'] + variaveis_controle], drop_first=True)
y_parede = df_parede['atraso']

# Padronizar variáveis numéricas
cols_numericas = ['pacientes_dia', 'exames_realizados', 'temp_medio_exame']
scaler_parede = StandardScaler()
X_parede[cols_numericas] = scaler_parede.fit_transform(X_parede[cols_numericas])

# Treinar modelo
log_reg_parede = LogisticRegression(max_iter=1000, random_state=42)
log_reg_parede.fit(X_parede, y_parede)

# Obter coeficiente e odds ratio para parede laranja
idx_laranja = list(X_parede.columns).index('parede_laranja')
coef_laranja = log_reg_parede.coef_[0][idx_laranja]
odds_ratio_laranja = np.exp(coef_laranja)

print(f"\nCoeficiente da parede laranja: {coef_laranja:.4f}")
print(f"Odds Ratio da parede laranja: {odds_ratio_laranja:.4f}")

if odds_ratio_laranja > 1:
    print(f"Interpretação: Parede laranja AUMENTA o risco de atraso em {(odds_ratio_laranja-1)*100:.1f}%")
else:
    print(f"Interpretação: Parede laranja REDUZ o risco de atraso em {(1-odds_ratio_laranja)*100:.1f}%")

# Verificar significância estatística (aproximada)
# Calcular erro padrão aproximado
n = len(X_parede)
se_approx = 1 / np.sqrt(n)
z_score = coef_laranja / se_approx
p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

print(f"\nZ-score aproximado: {z_score:.4f}")
print(f"P-valor aproximado: {p_value:.4f}")

if p_value < 0.05:
    print("O efeito é estatisticamente significativo (p < 0.05)")
else:
    print("O efeito NÃO é estatisticamente significativo (p >= 0.05)")

# Análise adicional: interação com tipo de exame
print("\n" + "-"*40)
print("Análise por tipo de exame:")
print("-"*40)

for tipo in df_parede['tipo_exame'].unique():
    df_tipo = df_parede[df_parede['tipo_exame'] == tipo]
    tempo_laranja = df_tipo[df_tipo['parede_laranja'] == 1]['tempo_entrega_resultado'].mean()
    tempo_normal = df_tipo[df_tipo['parede_laranja'] == 0]['tempo_entrega_resultado'].mean()
    
    if not np.isnan(tempo_laranja) and not np.isnan(tempo_normal):
        diff = tempo_laranja - tempo_normal
        print(f"{tipo:15} | Diferença: {diff:6.2f}h | Com laranja: {tempo_laranja:.2f}h | Sem: {tempo_normal:.2f}h")