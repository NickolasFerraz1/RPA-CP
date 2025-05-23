# Integrantes
* Nickolas Ferraz - RM558458
* Sandron Oliveira - RM557172
* Marcos Paolucci - RM554941
* Paulo Carvalho - RM554562
* Lorena Bauer - RM555272
* Herbertt di Franco - RM556640

# Projeto: Web Scraping de produtos 

## Descrição

Este projeto tem como objetivo automatizar a coleta de dados de produtos no site **Mercado Livre** a partir de uma palavra-chave inicial. O processo é dividido em três fases principais:

### Fase 1 – Preparação e Geração de Sinônimos

- O sistema recebe uma palavra-chave como entrada.
- Gera uma lista de sinônimos utilizando uma fonte pré-definida (pode ser um arquivo local ou uma API pública).
- Os sinônimos devem manter o contexto original da busca.

### Fase 2 – Implementação da Busca no Mercado Livre

- Para cada termo gerado, o sistema realiza uma busca no Mercado Livre.
- Os resultados são coletados com técnicas de scraping, respeitando as políticas de acesso do site.
- A quantidade de anúncios coletados por consulta é limitada para manter a eficiência do processo.

### Fase 3 – Organização e Geração do Dataset

- Os dados coletados são organizados em um arquivo `.csv`.
- O arquivo gerado contém as seguintes colunas:
  - `termo_de_busca`
  - `titulo_produto`
  - `preco`
  - `link`

## Tecnologias utilizadas

- Python
- Bibliotecas para scraping - *FireCrawl* foi utilizado, mas alternativas como *BeautifulSoup* também são compatíveis.
- Pandas para manipulação de dados
- API do *ChatGPT* para geração de sinônimos, com suporte a alternativas como APIs públicas ou arquivos locais.
  
## Como executar

1. Clone o repositório.
2. Instale as dependências listadas em `requirements.txt`.
3. Utilize sua chave API do ChatGPT e do FireCrawl (free).
4. Execute o script principal (app.py) com uma palavra-chave como argumento.
5. Verifique o arquivo `.csv` gerado na pasta de saída.

## Observações

- O uso do scraping deve respeitar os Termos de Uso do Mercado Livre.
- A geração de sinônimos deve garantir que os termos mantêm o contexto da busca original.
