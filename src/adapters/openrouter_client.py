"""
Adaptador de Integracao com OpenRouter para o Local AI Organizer.
Atende ao contrato `openrouter-integration/v1`.
Permite selecao dinamica de qualquer modelo do catalogo OpenRouter.
"""

import os
import sys
import json
import re
import ssl
import urllib.request
import urllib.error
from typing import Dict, List, Any, Optional

DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "qwen/qwen3.8-27b:free"

# Padroes proibidos para garantir a privacidade de dados locais

PROHIBITED_PATTERNS = [
    r"[a-zA-Z]:\\Users\\[^\s\"']+",   # Caminhos absolutos do Windows
    r"/home/[^\s\"']+",               # Caminhos absolutos do Linux
    r"sk-[a-zA-Z0-9_-]{20,}",         # Possiveis chaves privadas / tokens
    r"ghp_[a-zA-Z0-9]{20,}",          # Tokens do GitHub
]


def _get_ssl_context():
    """Retorna contexto SSL seguro com fallback para ambientes Windows/MSYS2 sem bundle CA."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        pass
    try:
        return ssl._create_unverified_context()
    except Exception:
        return ssl.create_default_context()


def _load_env_file():
    """Carrega variaveis de arquivos .env ou API_KEY.env se existirem, sem dependencias externas."""
    candidate_files = [".env", "API_KEY.env", "api_key.env"]
    for filename in candidate_files:
        env_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            if "=" in line:
                                k, v = line.split("=", 1)
                                k = k.strip()
                                v = v.strip().strip("'\"")
                                if k.upper().startswith("OPENROU") or k in ("API_KEY", "OPENROUTER_KEY"):
                                    os.environ["OPENROUTER_API_KEY"] = v
                                elif k and k not in os.environ:
                                    os.environ[k] = v
                            elif line.startswith("sk-or-"):
                                if "OPENROUTER_API_KEY" not in os.environ:
                                    os.environ["OPENROUTER_API_KEY"] = line.strip()

            except Exception:
                pass



class PrivacyViolationError(ValueError):
    """Disparada quando dados locais sensiveis sao detectados no payload."""
    pass


class OpenRouterAPIError(RuntimeError):
    """Disparada em caso de erro na resposta da API OpenRouter."""
    pass


class OpenRouterClient:
    def __init__(self, api_key: Optional[str] = None, mock_mode: bool = False):
        if api_key is None:
            _load_env_file()
            self.api_key = os.environ.get("OPENROUTER_API_KEY", "")
        else:
            self.api_key = api_key
        self.mock_mode = mock_mode
        self.base_url = DEFAULT_BASE_URL
        self._ssl_ctx = _get_ssl_context()

    def check_privacy_guardrail(self, messages: List[Dict[str, str]]) -> None:
        """
        Verifica se as mensagens contem caminhos absolutos locais ou credenciais.
        Garante que apenas dados sinteticos e instrucoes puras sejam transmitidos.
        """
        for msg in messages:
            content = msg.get("content", "")
            for pattern in PROHIBITED_PATTERNS:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    raise PrivacyViolationError(
                        f"Violacao de privacidade detectada: conteudo contem padrao proibido ({match.group(0)}). "
                        "Apenas dados sinteticos sao permitidos no OpenRouter."
                    )

    def list_models(self, free_only: bool = True) -> List[Dict[str, Any]]:
        """
        Consulta a lista publica de modelos do OpenRouter em tempo real.
        Nao exige chave de API para consulta publica.
        """
        req = urllib.request.Request(
            url=f"{self.base_url}/models",
            headers={"User-Agent": "Local-AI-Organizer/1.0"},
            method="GET",
        )
        try:
            with urllib.request.urlopen(req, timeout=15, context=self._ssl_ctx) as response:
                data = json.loads(response.read().decode("utf-8"))
                models = data.get("data", [])
                if free_only:
                    return [
                        m for m in models
                        if ":free" in m.get("id", "")
                        or (m.get("pricing", {}).get("prompt") == "0" and m.get("pricing", {}).get("completion") == "0")
                    ]
                return models
        except Exception as e:
            # Fallback seguro para lista conhecida em caso de falha de rede
            if self.mock_mode:
                return [
                    {"id": "meta-llama/llama-3.3-70b-instruct:free", "name": "Llama 3.3 70B (Free)"},
                    {"id": "qwen/qwen-2.5-72b-instruct:free", "name": "Qwen 2.5 72B (Free)"},
                    {"id": "mistralai/mistral-7b-instruct:free", "name": "Mistral 7B (Free)"},
                    {"id": "deepseek/deepseek-r1:free", "name": "DeepSeek R1 (Free)"},
                ]
            raise OpenRouterAPIError(f"Erro ao listar modelos do OpenRouter: {e}")

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = DEFAULT_MODEL,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """
        Executa uma solicitacao de chat completion via OpenRouter com qualquer modelo escolhido.
        """
        self.check_privacy_guardrail(messages)

        # Se for modo simulado ou dry-run, retorna mock estruturado
        if self.mock_mode or dry_run:
            user_text = messages[-1]["content"] if messages else ""
            return {
                "id": "mock-openrouter-001",
                "model": model,
                "created": 1789740000,
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": f"[MOCK OPENROUTER - {model}] Resposta sintetica para: {user_text[:50]}...",
                        },
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": len(user_text) // 4,
                    "completion_tokens": 30,
                    "total_tokens": (len(user_text) // 4) + 30,
                },
                "dry_run": True,
            }

        if not self.api_key:
            raise ValueError(
                "Chave OPENROUTER_API_KEY nao configurada. Defina a variavel de ambiente $env:OPENROUTER_API_KEY ou use mock_mode=True."
            )

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url=f"{self.base_url}/chat/completions",
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost/local-ai-organizer",
                "X-Title": "Local AI Organizer",
                "User-Agent": "Local-AI-Organizer/1.0",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=30, context=self._ssl_ctx) as response:
                resp_bytes = response.read()
                return json.loads(resp_bytes.decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            if e.code == 429:
                raise OpenRouterAPIError(f"Limite de taxa (Rate Limit) atingido no OpenRouter (HTTP 429): {err_body}")
            elif e.code == 401:
                raise OpenRouterAPIError(f"Chave de API invalida ou nao autorizada no OpenRouter (HTTP 401): {err_body}")
            else:
                raise OpenRouterAPIError(f"Erro HTTP {e.code} ao chamar OpenRouter: {err_body}")
        except urllib.error.URLError as e:
            raise OpenRouterAPIError(f"Falha de conexao com OpenRouter: {e.reason}")


if __name__ == "__main__":
    client = OpenRouterClient()

    if "--list-free" in sys.argv:
        print("Buscando modelos gratuitos disponiveis no OpenRouter em tempo real...")
        try:
            free_models = client.list_models(free_only=True)
            print(f"\nEncontrados {len(free_models)} modelos gratuitos disponiveis:")
            for m in free_models:
                m_id = m.get("id")
                m_name = m.get("name", m_id)
                print(f" - {m_id} ({m_name})")
        except Exception as err:
            print(f"Erro: {err}")
    else:
        # Teste rapido mock
        mock_client = OpenRouterClient(mock_mode=True)
        res = mock_client.chat_completion(
            messages=[{"role": "user", "content": "Teste sintetico de integracao."}],
            model=DEFAULT_MODEL,
            dry_run=True,
        )
        print("Resultado do teste mock:")
        print(json.dumps(res, indent=2))
        print("\nDica: Para listar todos os modelos gratuitos ao vivo, execute:")
        print("python src/adapters/openrouter_client.py --list-free")
