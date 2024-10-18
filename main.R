library(jsonlite)
library(arules)

normalizar_produtos <- function(produtos) {
  produtos_normalizados <- gsub("Refri .*", "Refri", produtos)
  produtos_normalizados <- gsub("Café .*", "Café", produtos_normalizados)
  produtos_normalizados <- gsub("Presunto .*", "Presunto", produtos_normalizados)
  produtos_normalizados <- gsub("Queijo .*", "Queijo", produtos_normalizados)
  produtos_normalizados <- gsub("Pão .*", "Pão", produtos_normalizados)
  produtos_normalizados <- gsub("Pastel .*", "Pastel", produtos_normalizados)
  produtos_normalizados <- gsub("Doce .*", "Doce", produtos_normalizados)
  
  return(produtos_normalizados)
}

processar_dados_padaria <- function(arquivo_json) {
  data <- fromJSON(arquivo_json, simplifyDataFrame = FALSE)
  
  compras <- lapply(data, function(x) normalizar_produtos(x$produtos))
  
  transacoes <- as(compras, "transactions")
  
  return(transacoes)
}

arquivo_json <- "padaria_trab.json"
transacoes_normalizadas <- processar_dados_padaria(arquivo_json)

regras <- apriori(transacoes_normalizadas, parameter = list(supp = 0.1, conf = 0.2))

inspect(regras)
