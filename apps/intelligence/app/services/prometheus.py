import re
import json
from typing import List, Dict, Any

# Strict UUID validation to prevent injection via IDs
UUID_REGEX = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

# Patterns to block in AI output to prevent phishing and data leakage
BLOCKED_PATTERNS = [
    r"https?://[^\s]+",  # Block all URLs
    r"seed phrase",
    r"private key",
    r"mnemonic",
    r"secret key",
    r"password",
]

def validate_id(id_str: str) -> str:
    """Validates that a string is a valid UUID."""
    if not UUID_REGEX.match(id_str):
        raise ValueError(f"Invalid ID format: {id_str}. Expected UUID.")
    return id_str

def construct_safe_prompt(system_instructions: str, user_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Constructs a prompt by passing user data as a structured JSON object.
    This separates data from instructions, mitigating prompt injection.
    """
    # Sanitize user data by ensuring IDs are valid
    if "userId" in user_data:
        validate_id(user_data["userId"])
    if "vaultId" in user_data:
        validate_id(user_data["vaultId"])

    return [
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": f"Context Data (JSON): {json.dumps(user_data)}"}
    ]

def filter_ai_output(text: str) -> str:
    """
    Filters AI output to remove sensitive patterns or malicious content.
    """
    filtered_text = text
    for pattern in BLOCKED_PATTERNS:
        filtered_text = re.sub(pattern, "[REDACTED]", filtered_text, flags=re.IGNORECASE)
    
    # Additional check for common phishing phrases
    if "click here" in filtered_text.lower() or "verify your account" in filtered_text.lower():
        filtered_text = "The AI response was blocked due to safety concerns."
        
    return filtered_text
