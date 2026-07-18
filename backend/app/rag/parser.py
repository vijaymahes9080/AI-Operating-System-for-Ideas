# backend/app/rag/parser.py
import re
from typing import List, Dict, Tuple

class LocalFileParser:
    @staticmethod
    def extract_text(file_content: bytes, filename: str) -> str:
        """Simple text extractor based on file types. (Fallback to text encoding)"""
        # Supports txt, markdown, csv, or reads bytes as utf-8 decode
        try:
            return file_content.decode("utf-8", errors="ignore")
        except Exception:
            return f"Binary file placeholder content: {filename}"

    @staticmethod
    def semantic_chunking(text: str, chunk_size: int = 800) -> List[str]:
        """Splits documents into semantic units by paragraph boundaries."""
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = []
        current_length = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            para_len = len(para)
            if current_length + para_len > chunk_size and current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = [para]
                current_length = para_len
            else:
                current_chunk.append(para)
                current_length += para_len
                
        if current_chunk:
            chunks.append("\n\n".join(current_chunk))
            
        return chunks

class PIIPrivacyFilter:
    def __init__(self):
        # Basic PII regex matching patterns (emails, keys, passwords)
        self.patterns = {
            "EMAIL": r'[\w\.-]+@[\w\.-]+\.\w+',
            "API_KEY": r'(?i)(api[-_]?key|secret|token|password|passwd)\s*[:=]\s*["\']([a-zA-Z0-9_\-\.]{16,})["\']'
        }

    def redact_payload(self, text: str) -> Tuple[str, Dict[str, str]]:
        """Redacts emails and api keys replacing them with metadata placeholders."""
        redacted = text
        mapping = {}
        
        for label, pattern in self.patterns.items():
            matches = re.findall(pattern, redacted)
            for idx, match in enumerate(matches):
                # If tuple match (like API keys regex groupings), select secret token
                target = match[1] if isinstance(match, tuple) else match
                placeholder = f"[{label}_REDACTED_{idx}]"
                mapping[placeholder] = target
                redacted = redacted.replace(target, placeholder)
                
        return redacted, mapping

    def restore_payload(self, redacted_text: str, mapping: Dict[str, str]) -> str:
        """Hydrates redacted tokens back to original values."""
        restored = redacted_text
        for placeholder, original in mapping.items():
            restored = restored.replace(placeholder, original)
        return restored
