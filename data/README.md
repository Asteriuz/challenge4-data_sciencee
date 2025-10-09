# Dicionário de Dados (Dataset fornecido)

| Variável                   | Tipo       | Descrição                                                                                              |
| -------------------------- | ---------- | ------------------------------------------------------------------------------------------------------ |
| unidade                    | categórica | Nome da unidade de atendimento Dasa (ex: Unidade A, Unidade B, ...)                                    |
| mes                        | categórica | Mês/ano da observação (ex: jan/2025)                                                                   |
| tipo_exame                 | categórica | Tipo principal de exame realizado (sangue, urina, imagem, genético, covid, hormonal, alergia)          |
| pacientes_dia              | numérica   | Número médio de pacientes atendidos por dia                                                            |
| exames_realizados          | numérica   | Número total de exames processados na unidade no mês                                                   |
| turno_mais_movimentado     | categórica | Turno com maior movimento (manhã, tarde, noite)                                                        |
| temp_medio_exame           | numérica   | Tempo médio para realização do exame, em minutos                                                       |
| protocolo_emergencia       | categórica | Indica se houve protocolo de emergência no período (sim/não)                                           |
| direcao_centrifuga         | categórica | Direção em que a centrífuga principal está voltada (leste, oeste, norte, sul)                          |
| quantidade_refrigeradores  | numérica   | Quantidade de refrigeradores presentes no laboratório (1 a 4)                                          |
| alinhamento_refrigeradores | categórica | Arranjo dos refrigeradores no espaço (lado_a_lado, em_L, dispersos)                                    |
| cor_parede_laboratorio     | categórica | Cor predominante da parede do laboratório (laranja, azul, verde, etc.)                                 |
| cor_parede_coleta          | categórica | Cor da parede da sala de coleta (branca, amarela, azul_cobalto, laranja, roxa, verde)                  |
| aromatizador_eucalipto     | categórica | Presença de aromatizador de eucalipto no laboratório (sim/não)                                         |
| cheiro_ambiente            | categórica | Cheiro predominante do ambiente (eucalipto, lavanda, café, nenhum)                                     |
| musica_ambiente            | categórica | Música tocando no laboratório (pagode_90s, jazz, rock, nenhuma)                                        |
| cor_jaleco_funcionario     | categórica | Cor do jaleco dos funcionários (verde_limao, branco, azul_bebe, vinho)                                 |
| elemento_decorativo        | categórica | Elemento decorativo no laboratório (vaso_bambu, samambaia, nenhum, cacto)                              |
| janela_virada_para         | categórica | Direção para a qual a janela principal do laboratório está voltada (leste, oeste, norte, sul, nenhuma) |
| hora_inicio_turno          | numérica   | Hora de início do turno mais movimentado (5 a 12)                                                      |
| cpf_biomedico              | numérica   | CPF do biomédico responsável (campo fictício, gerado aleatoriamente)                                   |
| mes_nascimento_biomedico   | categórica | Mês de nascimento do biomédico responsável (jan, fev, ..., dez)                                        |
| dia_fechamento             | numérica   | Dia do mês em que a unidade realiza o fechamento de rotina (1 a 31)                                    |
| chefe_setor                | categórica | Nome (ou número) do chefe do setor                                                                     |
| tipo_refrigeracao          | categórica | Tipo de refrigeração do laboratório (seca, umida, controlada, climatizada)                             |
| tempo_entrega_resultado    | numérica   | TARGET: Tempo em horas até a entrega do resultado ao paciente                                          |
