# scripts
Repositório criado para versionar e registrar scripts diversos que crio no dia a dia. 

# Exemplos
Scripts de automação RPA, utilitários pro dia a dia, solicitações de amigos para facilitar a rotina diária.
Esse repositório irá armazenar todos os scripts que forem sendo criados com o objetivo de resolver problemas pontuais.

# Script 1: Importação de dados - tratamento e montagem de planilha para importação em sistema
Esse script foi solicitado para facilitar o processo de geração de uma planilha que precisa ser importada para um sistema WEB. 
O usuário recebe as planilhas base do cliente (dados originais), o script faz a leitura e o processamento dos dados e gera as planilhas prontas 
  para a importação no sistema.

O script é executado no terminal e fica dessa forma: 

##################### IMPORTADOR DE DADOS PET #####################

INFORME OS DADOS SOLICITADOS PARA GERAR A PLANILHA PARA IMPORTAÇÃO

###################################################################

Digite o nome do arquivo CSV com os dados dos TUTORES enviado pelo cliente: clientes_3

Digite o nome do arquivo de saída para os TUTORES: saida_clientes_3

Digite a quantidade de linhas que cada planilha de TUTORES vai ter: 300

Foram encontrados 21 registros duplicados.

Arquivo 'saida_clientes_3_1.xlsx' gerado com 300 linhas.

Arquivo 'saida_clientes_3_2.xlsx' gerado com 300 linhas.

Arquivo 'saida_clientes_3_3.xlsx' gerado com 31 linhas.

##########################################################################

Planilha saida_clientes_3 gerada com sucesso!

Importe os dados da planilha gerada acima para o sistema. Após a importação, siga para os próximos passos

############################################################################################################

Digite o nome do arquivo CSV com os dados dos PETS enviado pelo cliente: animais_3

Digite o nome do arquivo EXCEL com os dados das RAÇAS (exportado do sistema modelo pet): base_modelo

Digite o nome do arquivo de saída para os PETS: saida_animais_3

Digite a quantidade de linhas que cada planilha de PETS vai ter: 300

Foram encontrados 95 registros duplicados.

Arquivo 'saida_animais_3_1.xlsx' gerado com 300 linhas.

Arquivo 'saida_animais_3_2.xlsx' gerado com 300 linhas.

Arquivo 'saida_animais_3_3.xlsx' gerado com 153 linhas.

##########################################################################

Planilha saida_animais_3 gerada com sucesso!

Exportação completa, as planilhas geradas podem ser importadas para o sistema
