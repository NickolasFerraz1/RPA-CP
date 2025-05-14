import os
import csv
import re

PASTA_TXT = R"C:\Users\nicko\OneDrive\Área de Trabalho\FIAP\Projetos\RPA\textos"  # ou o caminho onde estão os arquivos
ARQUIVO_CSV = "dados_mercado_livre.csv"

def extrair_dados_de_arquivo(caminho_arquivo, termo_de_busca):
    resultados = []

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Expressão para encontrar todos os blocos com título, link e preço
    blocos = re.findall(
        r"### \[(.*?)\]\((.*?)\).*?\n+.*?R\$([\d\.,]+)",  # Novo padrão
        conteudo,
        re.DOTALL
    )

    for titulo, link, preco in blocos:
        resultados.append({
            "termo_de_busca": termo_de_busca,
            "titulo_produto": titulo.strip(),
            "descricao": "",  # Pode ser preenchido depois se necessário
            "preco": preco.replace(".", "").replace(",", "."),
            "link": link.strip()
        })

    return resultados

def gerar_csv():
    todos_dados = []

    for nome_arquivo in os.listdir(PASTA_TXT):
        if nome_arquivo.endswith(".txt"):
            caminho = os.path.join(PASTA_TXT, nome_arquivo)
            termo = nome_arquivo.replace(".txt", "").replace("-", " ")
            try:
                dados = extrair_dados_de_arquivo(caminho, termo)
                if not dados:
                    print(f"⚠️ Nenhum dado encontrado em: {nome_arquivo}")
                else:
                    print(f"✅ {len(dados)} itens encontrados em: {nome_arquivo}")
                todos_dados.extend(dados)
            except Exception as e:
                print(f"❌ Erro ao processar {nome_arquivo}: {e}")

    if todos_dados:
        with open(ARQUIVO_CSV, 'w', newline='', encoding='utf-8') as csvfile:
            campos = ["termo_de_busca", "titulo_produto", "descricao", "preco", "link"]
            writer = csv.DictWriter(csvfile, fieldnames=campos)
            writer.writeheader()
            writer.writerows(todos_dados)
        print(f"\n📁 CSV gerado com sucesso: {ARQUIVO_CSV}")
    else:
        print("\n⚠️ Nenhum dado foi extraído. Verifique os arquivos.")

if __name__ == "__main__":
    gerar_csv()
