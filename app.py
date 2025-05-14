import openai
from openai import OpenAI
from firecrawl import FirecrawlApp

# 🔐 Chaves da API
OPENAI_API_KEY = "SUA-CHAVE-API"
FIRECRAWL_API_KEY = "SUA-CHAVE-API"

# Inicializa os clientes
client = OpenAI(api_key=OPENAI_API_KEY)
firecrawl_app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# 🔁 Função para gerar sinônimos
def gerar_sinonimos_com_gpt4o(palavra_chave):
    prompt = f"Liste sinônimos contextuais em português para a palavra '{palavra_chave}'. Apenas a lista separada por vírgulas."

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",  # Ou "gpt-3.5-turbo" se preferir
        messages=[
            {"role": "system", "content": (
    "Você é um especialista em cartuchos de tinta, toners, impressoras jato de tinta e laser, manutenção, suprimentos e compatibilidades. "
    "Seu trabalho é fornecer respostas técnicas e práticas em português, ajudando a encontrar sinônimos, esclarecer dúvidas técnicas, "
    "e orientar sobre o uso correto de produtos relacionados a impressão. Seja claro, objetivo e contextualizado para o setor de impressoras."
    "Você vai me passar palavras que tenham relação com impressora, para que eu faça uma busca na internet e a palavra me retorne algo relacionado à impressoras"
    "A palavra será usada em uma busca, logo quando eu colocá-la na internet, deverá me retornar algo relacionado com impressoras"
    '''Exemplos: {"role": "user", "content": "Cartucho hp"} {"role": "assistant", "content": Tinta de Impressora, Cartucho de Tinta, Reservatório de Tinta, Toner, Recarga de Cartucho, Refil de Tinta de Impressora}'''
)},

            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=100
    )

    # Retorna lista de sinônimos, já limpa
    texto = resposta.choices[0].message.content.strip()
    sinonimos = [s.strip().lower() for s in texto.split(",") if s.strip()]
    return sinonimos

# 🕸️ Função para buscar e salvar resultados do Mercado Livre
def buscar_e_salvar_dados(sinonimos):
    for palavra in sinonimos:
        palavra_formatada = palavra.replace(" ", "-")
        palavra_parametro = palavra.replace(" ", "%20")
        url = f"https://lista.mercadolivre.com.br/{palavra_formatada}#D[A:{palavra_parametro}]"
        
        print(f"🔎 Buscando por: {palavra} -> {url}")
        
        try:
            scrape_result = firecrawl_app.scrape_url(url=url, formats=['markdown'])
            with open(f'{palavra_formatada}.txt', 'w', encoding='utf-8') as f:
                f.write(scrape_result.markdown)
            print(f"✅ Resultado salvo em {palavra_formatada}.txt\n")
        except Exception as e:
            print(f"❌ Erro ao buscar '{palavra}': {e}\n")

# 🚀 Execução principal
if __name__ == "__main__":
    palavra_base = input("Digite uma palavra-chave para gerar sinônimos: ")
    lista_sinonimos = gerar_sinonimos_com_gpt4o(palavra_base)
    print(f"\n🔠 Sinônimos encontrados: {', '.join(lista_sinonimos)}\n")
    buscar_e_salvar_dados(lista_sinonimos)
