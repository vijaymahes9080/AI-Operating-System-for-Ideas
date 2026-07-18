# Prompt Engineering Framework

To ensure that IdeasOS agents produce deterministic, high-quality, and structurally valid outputs, we implement a strict **Prompt Template System** featuring role isolation, Pydantic verification, and system boundaries.

---

## 1. System Prompt Library

Each specialized agent has an isolated system prompt written to enforce structured schema formats.

### Core System Instruction: Research Agent
```
Role: Senior Research Librarian & Market Intelligence Officer
Context: You run within the IdeasOS system.
Objective: Analyze raw user concept statements and locate real academic papers, competitors, and technical benchmarks.

Rules:
1. Always output structured metadata.
2. NEVER synthesize or hallucinate external links, names of competitors, or libraries. If you cannot find a source, state 'SOURCE_NOT_FOUND'.
3. Verify licensing of mentioned GitHub repositories and libraries.
```

### Core System Instruction: Architect Agent
```
Role: Principal Systems Architect & Cryptographer
Objective: Convert a set of features and research metrics into a production-grade database, API, and deployment spec.

Rules:
1. Prioritize open-source, local-first stacks (FastAPI, SQLite, SQLite-vec, Neo4j, Tauri).
2. Detail threat mitigations (SQL injection, XSS, LLM Prompt Injection).
3. Do not output placeholder comments in schema files. Write fully executable SQL/TS types.
```

---

## 2. Dynamic Input/Output Context Templates

Prompt payloads are assembled dynamically inside the backend service using strict delimiters to separate context from instructions:

```
=== AGENT SYSTEM ROLE ===
{agent_system_instructions}

=== PROJECT CURRENT KNOWLEDGE STATE ===
Project Name: {project_name}
Metadata Hash: {project_dna}

--- KNOWLEDGE GRAPH SUB-EXTRACT ---
{knowledge_graph_json}

--- SEARCH EVIDENCE RAG RESULTS ---
{rag_results_markdown}

=== CURRENT USER COMMAND ===
{user_command}

=== RESPONSE CONSTRAINTS ===
You MUST respond with a single valid JSON object containing precisely the structure defined in the JSON Schema.
Do not wrap JSON inside markdown blocks (do not use ```json).
```

---

## 3. Pydantic Structured Output Validation

To prevent LLM formatting drift (e.g., incomplete brackets, incorrect schema types), the engine uses Pydantic models for structured output parsing.

```python
# backend/app/agents/schemas.py
from typing import List, Optional
from pydantic import BaseModel, Field, conlist

class CompetitorSchema(BaseModel):
    name: str = Field(description="Name of the competitor platform or open source project")
    url: str = Field(description="URL to competitor website or GitHub repository")
    strengths: List[str] = Field(description="Strengths of their implementation")
    weaknesses: List[str] = Field(description="Identified gaps where our idea is novel")

class ResearchOutputSchema(BaseModel):
    summary: str = Field(description="A 3-paragraph executive summary of the technology landscapre")
    academic_citations: List[str] = Field(description="Academic papers with citation metrics (arXiv, Semantic Scholar)")
    competitor_list: List[CompetitorSchema] = Field(description="List of direct and indirect competitors")
    required_skills: List[str] = Field(description="Developer skillsets required to build this project")
    suggested_license: str = Field(description="Legal licensing recommendation (e.g., MIT, AGPL-3.0, Apache-2.0)")

# Parser execution utility
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

def query_agent_with_validation(llm, prompt_text) -> ResearchOutputSchema:
    parser = JsonOutputParser(pydantic_object=ResearchOutputSchema)
    
    # Try query
    for attempt in range(3):
        try:
            raw_response = llm.invoke(prompt_text + f"\n\nJSON Schema:\n{parser.get_format_instructions()}")
            parsed_result = parser.parse(raw_response.content)
            return ResearchOutputSchema(**parsed_result)
        except (OutputParserException, ValueError) as e:
            # Self-correction loop: append error context and retry
            prompt_text += f"\n\nCorrection Notice: Your last output failed validation with error: {str(e)}. Please correct your JSON output."
            
    raise ValueError("Agent failed to output valid JSON schema after 3 correction loops.")
```
