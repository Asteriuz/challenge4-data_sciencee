import pandas as pd

COLUNAS_ORDENADAS = [
    # Context (Where and When)
    "unidade",
    "mes",
    "dia_fechamento",
    # Core Operations
    "pacientes_dia",
    "exames_realizados",
    "tipo_exame",
    "turno_mais_movimentado",
    "hora_inicio_turno",
    "temp_medio_exame",
    "tempo_entrega_resultado",
    # Equipment & Procedures
    "protocolo_emergencia",
    "quantidade_refrigeradores",
    "tipo_refrigeracao",
    "alinhamento_refrigeradores",
    "direcao_centrifuga",
    # Personnel
    "chefe_setor",
    "cpf_biomedico",
    "cor_jaleco_funcionario",
    "mes_nascimento_biomedico",
    # Environmental Ambiance
    "musica_ambiente",
    "cheiro_ambiente",
    "aromatizador_eucalipto",
    "elemento_decorativo",
    # Physical Infrastructure
    "cor_parede_laboratorio",
    "cor_parede_coleta",
    "janela_virada_para",
]


def format_float(value):
    """Formata números com ponto como separador de milhares e vírgula como decimal"""
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_integer(value):
    """Formata inteiros com ponto como separador de milhares"""
    return f"{value:,}".replace(",", ".")

def get_dimensions(df: pd.DataFrame) -> str:
    return f"{format_integer(df.shape[0])} registros, {format_integer(df.shape[1])} colunas"

def generate_unique_values_table(df):
    colunas_selecionadas = df.select_dtypes(
        include=["object", "bool", "category", "boolean"]
    ).columns

    if colunas_selecionadas.empty:
        return "Nenhuma coluna do tipo object, bool, category ou boolean encontrada."

    data_valores_unicos = []

    for coluna in colunas_selecionadas:
        value_counts = df[coluna].value_counts(dropna=False)

        if len(value_counts) < 100:
            values_list = [
                "NaN" if pd.isna(val) else str(val) for val in value_counts.index
            ]
            data_valores_unicos.append({"Coluna": coluna, "Valores": values_list})

    if not data_valores_unicos:
        return "Nenhuma coluna com menos de 100 valores únicos encontrada."

    df_valores_unicos = pd.DataFrame(data_valores_unicos)

    markdown_table = "| Coluna                     | Valores |\n"
    markdown_table += "|----------------------------|---------|\n"
    for _, row in df_valores_unicos.iterrows():
        markdown_table += f"| {row['Coluna']:<28} | {', '.join(row['Valores'])} |\n"

    return markdown_table
