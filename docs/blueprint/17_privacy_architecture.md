# Privacy Architecture

IdeasOS is built around a **Privacy-First** design model. Users own their data. This specification details how local boundaries are maintained, how Personally Identifiable Information (PII) is redacted, and how GDPR/CCPA compliance is handled.

---

## 1. Local Data Boundaries

The architecture guarantees that all core intellectual property remains on the host machine by default:

- **Local Vector Database**: SQLite-vec performs semantic indices and retrieval fully on-device. No document text is sent to third-party vector databases.
- **Local Parsing**: Audio transcription (Whisper), text parsing (Apache Tika), and OCR (Tesseract) run as local Python subprocesses.
- **Opt-In Cloud Access**: Users must explicitly authorize external calls to APIs (such as OpenAI, Anthropic, or Tavily Web Search).

---

## 2. PII Redaction Filter

To protect sensitive information (e.g. phone numbers, email addresses, API tokens, security hashes, legal names) from being leaked to third-party LLMs, IdeasOS runs a pre-flight redaction filter:

```
[Prompt Context Payload]
           |
           v
[regex/Presidio Analyzer] ---> (PII Matches) ---> [Obfuscator Node] ---> [Redacted Payload] ---> [Cloud LLM API]
```

- **Technology**: Microsoft Presidio Analyzer or customized regex maps.
- **Action**: Identified sensitive values are replaced with placeholders (e.g., `[REDACTED_EMAIL_1]`) before the payload is sent over the network.
- **Re-hydration Hook**: When the LLM returns the structured response, the backend replaces the placeholders with the original values stored in memory before updating files or database tables.

```python
# backend/app/security/privacy.py
import re
from typing import Dict, Tuple

class PIIRedactor:
    def __init__(self):
        # Base Regex patterns for common sensitive values
        self.patterns = {
            "EMAIL": r'[\w\.-]+@[\w\.-]+\.\w+',
            "PHONE": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "API_KEY": r'(?i)(api[-_]?key|secret|token|password|passwd)\s*[:=]\s*["\']([a-zA-Z0-9_\-\.]{16,})["\']'
        }

    def redact(self, text: str) -> Tuple[str, Dict[str, str]]:
        mapping = {}
        redacted_text = text
        
        for pii_type, pattern in self.patterns.items():
            matches = re.findall(pattern, redacted_text)
            for idx, match in enumerate(matches):
                # Handle API key tuple from groups
                match_val = match[1] if isinstance(match, tuple) else match
                placeholder = f"[{pii_type}_REDACTED_{idx}]"
                mapping[placeholder] = match_val
                redacted_text = redacted_text.replace(match_val, placeholder)
                
        return redacted_text, mapping
```

---

## 3. GDPR and CCPA Compliance in Offline Systems

Although IdeasOS is local-first, it supports features to help developers stay compliant when deploying platforms:

- **Right to Be Forgotten**: Users can delete projects or workspaces at any time. When a workspace is deleted, the backend executes `PRAGMA secure_delete = ON` (overwriting deleted SQLite database pages with zeros) and physically deletes all files on disk.
- **Data Portability**: Users can export their entire Knowledge Graph, raw files, tasks, and decision ledgers as a single ZIP archive containing structured JSON and markdown files.
