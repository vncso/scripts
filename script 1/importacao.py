import pandas as pd
import openpyxl as xl
import python_calamine as cal

mapa_sinonimos = {
    'spitz alemão': 'Spitz Alemão Anão',
    'poodle micro': 'Poodle Toy',
    'yorkshire': 'Yorkshire Terrier',
    'Shih tzu': 'Shih-Tzu',
    'Bulldog Francês': 'Buldogue Francês',
    'Bulldog Americano': 'Buldogue Americano',
    'Bulldog Inglês': 'Buldogue Inglês',
    'Pinscher': 'Pinscher Miniatura'
}

print('##################### IMPORTADOR DE DADOS PET #####################')
print('INFORME OS DADOS SOLICITADOS PARA GERAR A PLANILHA PARA IMPORTAÇÃO')
print('###################################################################')
CSV_TUTORES = input('Digite o nome do arquivo CSV com os dados dos TUTORES enviado pelo cliente: ')
PLANILHA_SAIDA_TUT = input('Digite o nome do arquivo de saída para os TUTORES: ')
qtd_linhas = int(input('Digite a quantidade de linhas que cada planilha de TUTORES vai ter: '))
try:
    tutores = pd.read_csv(CSV_TUTORES+'.csv', sep=';') # INFORMAR NOME DA PLANILHA DE TUTORES DO CLIENTE
except FileNotFoundError as e:
    print(f'\nERRO: NÃO FOI POSSÍVEL ABRIR O ARQUIVO "{CSV_TUTORES}". VERIFIQUE SE O NOME ESTÁ CORRETO E SE O ARQUIVO ESTÁ NA MESMA PASTA DO SCRIPT.')
    print(e)

# dados_tutores = pd.read_excel('dados_pets_6993017b2414d.xlsx')
# dados_pets = pd.read_excel('dados_pets_699301e24b658.xlsx', engine='calamine', sheet_name='TUTORES')

df_dados_tutores = pd.DataFrame()

df_dados_tutores['NOME'] = tutores['Nome']
df_dados_tutores['SEXO'] = None
df_dados_tutores['CPF'] = tutores['CPF']
df_dados_tutores['RG'] = tutores['RG'].apply(lambda x: x if str(x).isnumeric() else None)
df_dados_tutores['TELEFONE'] = tutores['Telefone']
df_dados_tutores['CELULAR'] = tutores['Telefone']
df_dados_tutores['E-MAIL'] = tutores['Email']
df_dados_tutores['RUA'] = tutores['Endereco']
df_dados_tutores['NUMERO'] = tutores['Numero']
df_dados_tutores['BAIRRO'] = tutores['Bairro']
df_dados_tutores['CIDADE'] = tutores['Cidade']
df_dados_tutores['ESTADO'] = tutores['Estado']
df_dados_tutores['CEP'] = tutores['CEP']
df_dados_tutores['COMPLEMENTO'] = tutores['Complemento']

# Validação de registros duplicados
duplicados = df_dados_tutores[df_dados_tutores.duplicated(keep=False)]

if not duplicados.empty:
    print(f"Foram encontrados {len(duplicados)} registros duplicados.")
    duplicados.to_excel('tutores_duplicados.xlsx', index=False)

df_dados_tutores = df_dados_tutores.drop_duplicates()

# Tamanho máximo permitido pelo sistema de importação
tamanho_lote = qtd_linhas

# Loop para fatiar e salvar os arquivos
for i in range(0, len(df_dados_tutores), tamanho_lote):
    # Fatiamos o DataFrame da linha 'i' até 'i + 300'
    lote = df_dados_tutores.iloc[i: i + tamanho_lote]

    num_arquivo = (i // tamanho_lote) + 1
    nome_arquivo = f'{PLANILHA_SAIDA_TUT}_{num_arquivo}.xlsx'

    # Salva o arquivo atual
    lote.to_excel(nome_arquivo, index=False)

    print(f"Arquivo '{nome_arquivo}' gerado com {len(lote)} linhas.")


print('\n##########################################################################')
print(f'\nPlanilha {PLANILHA_SAIDA_TUT} gerada com sucesso!')
print('\nImporte os dados da planilha gerada acima para o sistema. Após a importação, siga para os próximos passos')
print('############################################################################################################')

CSV_PETS = input('\nDigite o nome do arquivo CSV com os dados dos PETS enviado pelo cliente: ')
XLS_RACAS = input('Digite o nome do arquivo EXCEL com os dados das RAÇAS (exportado do sistema modelo pet): ')
PLANILHA_SAIDA_PET = input('Digite o nome do arquivo de saída para os PETS: ')
qtd_linhas = int(input('Digite a quantidade de linhas que cada planilha de PETS vai ter: '))

try:
    pets = pd.read_csv(CSV_PETS+'.csv', sep=';') # INFORMAR NOME DA PLANILHA DE PETS DO CLIENTE
except FileNotFoundError as e:
    print(f'\nERRO: NÃO FOI POSSÍVEL ABRIR O ARQUIVO "{CSV_PETS}". VERIFIQUE SE O NOME ESTÁ CORRETO E SE O ARQUIVO ESTÁ NA MESMA PASTA DO SCRIPT.')
    print(e)

try:
    base_racas = pd.read_excel(XLS_RACAS+'.xlsx', engine='calamine', sheet_name='RAÇAS') # INFORMAR PLANILHA COM OS IDS DA RAÇA EXPORTADO DO SISTEMA
    base_tutores = pd.read_excel(XLS_RACAS+'.xlsx', engine='calamine', sheet_name='TUTORES')
except FileNotFoundError as e:
    print(f'\nERRO: NÃO FOI POSSÍVEL ABRIR O ARQUIVO "{XLS_RACAS}". VERIFIQUE SE O NOME ESTÁ CORRETO E SE O ARQUIVO ESTÁ NA MESMA PASTA DO SCRIPT.')
    print(e)

pets_tutores = pd.merge(pets, tutores, on='CdCliente', how='inner')

pets_tutores['Cliente'] = pets_tutores['Cliente'].str.upper().str.strip()
base_tutores['Cliente'] = base_tutores['NOME TUTOR'].str.upper().str.strip()

pets_tutores = pd.merge(
    pets_tutores,
    base_tutores[['Cliente', 'ID TUTOR']], # ADICIONADO 'Cliente' AQUI
    on='Cliente',
    how='left'
)

mapa_padronizado = {k.upper(): v.upper() for k, v in mapa_sinonimos.items()}

pets_tutores.rename(columns={'Raca': 'NOME RAÇA'}, inplace=True)

pets_tutores['NOME RAÇA'] = pets_tutores['NOME RAÇA'].str.upper().str.strip()

pets_tutores['NOME RAÇA'] = pets_tutores['NOME RAÇA'].replace(mapa_padronizado)

base_racas['NOME RAÇA'] = base_racas['NOME RAÇA'].str.upper().str.strip()

pets_tutores_final = pd.merge(pets_tutores, base_racas, on='NOME RAÇA', how='left')

df_dados_pets = pd.DataFrame()

df_dados_pets['ID TUTOR'] = pets_tutores['ID TUTOR']
df_dados_pets['NOME TUTOR'] = pets_tutores_final['Cliente']
df_dados_pets['NOME DO PET'] = pets_tutores_final['Nome_x']
df_dados_pets['ID RAÇA'] = pets_tutores_final['ID RAÇA']
df_dados_pets['APELIDO DO PET'] = pets_tutores_final['Nome_x']
df_dados_pets['SEXO'] = pets_tutores_final['Sexo']
df_dados_pets['DATA DE NASCIMENTO'] = pets_tutores_final['Nascimento_x']
df_dados_pets['COR'] = pets_tutores_final['Cor']
df_dados_pets['OBS'] = pets_tutores_final['Obs']
df_dados_pets['Castrado?'] = pets_tutores_final['Castrado']
df_dados_pets['PORTE'] = pets_tutores_final['Porte']
df_dados_pets['PESO (KG)'] = pets_tutores_final['Peso']
df_dados_pets['TREINADO?'] = None
df_dados_pets['PELAGEM'] = pets_tutores_final['Pelagem']
df_dados_pets['NOME DO VETERINARIO'] = None
df_dados_pets['CONTATO DO VETERINARIO'] = None

# Validação de registros duplicados
duplicados = df_dados_pets[df_dados_pets.duplicated(subset=['NOME TUTOR', 'NOME DO PET'], keep=False)]

if not duplicados.empty:
    print(f"Foram encontrados {len(duplicados)} registros duplicados.")
    duplicados.to_excel('pets_duplicados.xlsx', index=False)

df_dados_pets = df_dados_pets.drop_duplicates(subset=['NOME TUTOR', 'NOME DO PET'], keep='first')

tamanho_lote = qtd_linhas

# Loop para fatiar e salvar os arquivos
for i in range(0, len(df_dados_pets), tamanho_lote):
    # Fatiamos o DataFrame da linha 'i' até 'i + qtd_linhas'
    lote = df_dados_pets.iloc[i: i + tamanho_lote]

    num_arquivo = (i // tamanho_lote) + 1
    nome_arquivo = f'{PLANILHA_SAIDA_PET}_{num_arquivo}.xlsx'

    # Salva o arquivo atual
    lote.to_excel(nome_arquivo, index=False)

    print(f"Arquivo '{nome_arquivo}' gerado com {len(lote)} linhas.")

print('\n##########################################################################')
print(f'\nPlanilha {PLANILHA_SAIDA_PET} gerada com sucesso!')
print('\nExportação completa, as planilhas geradas podem ser importadas para o sistema')
