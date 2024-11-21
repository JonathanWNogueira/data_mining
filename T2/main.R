library(openxlsx)

arquivo <- "datasets/IO/CE.xls"

dados <- read_xls(arquivo)

print("Visualização dos primeiros registros:")
print(head(dados))
    
print("Informações gerais do arquivo:")
print(str(dados))

