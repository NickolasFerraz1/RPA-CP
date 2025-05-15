from openai import OpenAI
from firecrawl import FirecrawlApp
import os
import csv
import re

# 🔐 Chaves da API
OPENAI_API_KEY = "SUA-CHAVE-API"
FIRECRAWL_API_KEY = "SUA-CHAVE-API"

# Inicializa os clientes
client = OpenAI(api_key=OPENAI_API_KEY)
firecrawl_app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# 📁 Pasta para salvar os .txt
PASTA_TXT = "textos"
ARQUIVO_CSV = "dados_mercado_livre.csv"

# 🧹 Limpa a pasta "textos" antes de salvar novos arquivos
if os.path.exists(PASTA_TXT):
    for filename in os.listdir(PASTA_TXT):
        file_path = os.path.join(PASTA_TXT, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
else:
    os.makedirs(PASTA_TXT)

# 🔁 Gera sinônimos com GPT-4o
def gerar_sinonimos_com_gpt4o(palavra_chave):
    prompt = f"Liste sinônimos contextuais em português para a palavra '{palavra_chave}'. Apenas a lista separada por vírgulas."

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",  # ou "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": (
                "Você é um especialista em cartuchos de tinta, toners, impressoras jato de tinta e laser, manutenção, suprimentos e compatibilidades. "
                "Seu trabalho é fornecer respostas técnicas e práticas em português, ajudando a encontrar sinônimos, esclarecer dúvidas técnicas, "
                "e orientar sobre o uso correto de produtos relacionados a impressão. Seja claro, objetivo e contextualizado para o setor de impressoras. "
                "A palavra será usada em uma busca, logo deverá me retornar algo relacionado com impressoras na internet."
            )},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=100
    )

    texto = resposta.choices[0].message.content.strip()
    sinonimos = [s.strip().lower() for s in texto.split(",") if s.strip()]
    return sinonimos

# 🕸️ Faz scraping no Mercado Livre
def buscar_e_salvar_dados(sinonimos):
    os.makedirs(PASTA_TXT, exist_ok=True)
    for palavra in sinonimos:
        palavra_formatada = palavra.replace(" ", "-")
        palavra_parametro = palavra.replace(" ", "%20")
        url = f"https://lista.mercadolivre.com.br/{palavra_formatada}#D[A:{palavra_parametro}]"

        print(f"🔎 Buscando por: {palavra} -> {url}")

        try:
            scrape_result = firecrawl_app.scrape_url(url=url, formats=['markdown'])
            caminho_arquivo = os.path.join(PASTA_TXT, f'{palavra_formatada}.txt')
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                f.write(scrape_result.markdown)
            print(f"✅ Resultado salvo em {caminho_arquivo}\n")
        except Exception as e:
            print(f"❌ Erro ao buscar '{palavra}': {e}\n")

# 🧠 Extrai dados dos arquivos .txt
def extrair_dados_de_arquivo(caminho_arquivo, termo_de_busca):
    resultados = []

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    blocos = re.findall(
        r"### \[(.*?)\]\((.*?)\).*?\n+.*?R\$([\d\.,]+)",
        conteudo,
        re.DOTALL
    )

    for titulo, link, preco in blocos:
        resultados.append({
            "termo_de_busca": termo_de_busca,
            "titulo_produto": titulo.strip(),
            "preco": preco.replace(".", "").replace(",", "."),
            "link": link.strip()
        })

    return resultados

# 🗃️ Gera CSV com os dados extraídos
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
            campos = ["termo_de_busca", "titulo_produto", "preco", "link"]
            writer = csv.DictWriter(csvfile, fieldnames=campos)
            writer.writeheader()
            writer.writerows(todos_dados)
        print(f"\n📁 CSV gerado com sucesso: {ARQUIVO_CSV}")
    else:
        print("\n⚠️ Nenhum dado foi extraído. Verifique os arquivos.")

# 🚀 Execução principal
if __name__ == "__main__":
    palavra_base = input("Digite uma palavra-chave para gerar sinônimos: ")
    lista_sinonimos = gerar_sinonimos_com_gpt4o(palavra_base)
    print(f"\n🔠 Sinônimos encontrados: {', '.join(lista_sinonimos)}\n")

    buscar_e_salvar_dados(lista_sinonimos)
    gerar_csv()
