library(openxlsx)

path <- "datasets/Diciplinas/"  

arquivos <- list.files(path = path, pattern = "\\.xls", full.names = TRUE)

dados_combinados <- data.frame()

for (arquivo in arquivos) {  
  
  dados <- read.xlsx(arquivo)
  dados$Arquivo_Origem <- basename(arquivo)
  dados_combinados <- rbind(dados_combinados, dados)

}

cat("\n### Dados combinados (visualização inicial): ###\n")
print(head(dados_combinados))

output_arquivo <- "diciplinas.xlsx"
write.xlsx(dados_combinados, file = output_arquivo)
