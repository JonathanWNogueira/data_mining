library(openxlsx)

path <- "datasets/IO/"  

arquivos <- list.files(path = path, pattern = "\\.xlsx", full.names = TRUE)

dados_combinados <- data.frame()

for (arquivo in arquivos) {  
  
  dados <- read.xlsx(arquivo)
  dados$Arquivo_Origem <- basename(arquivo)
  dados_combinados <- rbind(dados_combinados, dados)

}

cat("\n### Dados combinados (visualização inicial): ###\n")
print(head(dados_combinados))

output_arquivo <- "io.xlsx"
write.xlsx(dados_combinados, file = output_arquivo)
