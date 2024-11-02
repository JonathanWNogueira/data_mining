library(jsonlite)
library(arules)
library(knitr)

normalizar_produtos <- function(produtos) {
  padroes <- c("Refri .*", "Café .*", "Presunto .*", "Queijo .*", "Pão .*", "Pastel .*", "Doce .*")
  substituicoes <- c("Refri", "Café", "Presunto", "Queijo", "Pão", "Pastel", "Doce")

  for (i in seq_along(padroes)) {
    produtos <- gsub(padroes[i], substituicoes[i], produtos)
  }
  
  return(produtos)
}

processar_dados_padaria <- function(arquivo_json) {
  data <- fromJSON(arquivo_json, simplifyDataFrame = FALSE)
  
  compras <- lapply(data, function(x) normalizar_produtos(x$produtos))
  
  transacoes <- as(compras, "transactions")
  
  return(transacoes)
}

arquivo_json <- "padaria_trab.json"

transacoes_normalizadas <- processar_dados_padaria(arquivo_json)

regras <- apriori(transacoes_normalizadas, parameter = list(supp = 0.04, conf = 0.6))
#regras <- subset(regras, rhs %pin% "Doce" & size(lhs) > 0)
regras <- head(sort(regras, by = "confidence"), 5)

tabela_regras <- as(regras, "data.frame")
print(kable(tabela_regras))