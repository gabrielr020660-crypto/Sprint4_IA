import re

INJECTION_PATTERNS = [
    r"ignore (all )?previous instructions",
    r"você agora é",
    r"dan mode",
    r"system prompt"
]

def checar_jailbreak(mensagem: str) -> bool:
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, mensagem, re.IGNORECASE):
            return True
    return False