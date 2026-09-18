"""
Script de exemplo para conversar com modelos do OpenRouter.
Você pode abrir e editar este arquivo quando quiser testar novos modelos!
"""

import os
from src.adapters.openrouter_client import OpenRouterClient

# 1. ESCOLHA O MODELO QUE VOCÊ QUER TESTAR
# Dica: rode 'python src/adapters/openrouter_client.py --list-free' para ver a lista completa
MODELO_ESCOLHIDO = "qwen/qwen3.8-27b:free"
# Outros exemplos que você pode experimentar:
# MODELO_ESCOLHIDO = "deepseek/deepseek-v4-flash-0731:free"
# MODELO_ESCOLHIDO = "nvidia/nemotron-3.5-lightning:free"
# MODELO_ESCOLHIDO = "google/gemma-4-31b-it:free"

# 2. SUA MENSAGEM / PERGUNTA
MENSAGEM = "Olá! Explique o que é uma API REST em duas frases simples."


def main():
    client = OpenRouterClient()

    if not client.api_key:
        print("----------------------------------------------------------------------")
        print("AVISO: Nenhuma chave 'OPENROUTER_API_KEY' foi encontrada no ambiente.")
        print("Rodando em modo SIMULADO (MOCK) para demonstrar o funcionamento.")
        print("Quando tiver sua chave real, você pode:")
        print(' 1. No terminal: $env:OPENROUTER_API_KEY = "sua_chave_aqui"')
        print(' 2. Ou criar um arquivo .env na pasta com: OPENROUTER_API_KEY=sua_chave_aqui')
        print("----------------------------------------------------------------------\n")
        client.mock_mode = True
    else:
        print(f"Chave detectada! Conectando ao OpenRouter com o modelo: {MODELO_ESCOLHIDO}...\n")

    # 3. ENVIA A MENSAGEM E RECEBE A RESPOSTA
    resposta = client.chat_completion(
        messages=[{"role": "user", "content": MENSAGEM}],
        model=MODELO_ESCOLHIDO,
    )

    conteudo = resposta["choices"][0]["message"]["content"]
    print("--- RESPOSTA DA IA ---")
    print(conteudo)
    print("-----------------------")


if __name__ == "__main__":
    main()
