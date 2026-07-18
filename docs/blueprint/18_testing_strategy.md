# Testing Strategy & QA

To build a reliable platform, IdeasOS implements a multi-layered testing strategy combining unit tests, end-to-end (E2E) integration checks, performance benchmarking, and agentic regression tests.

---

## 1. Test Automation Matrix

| Layer | Target | Framework | Command |
|---|---|---|---|
| **Backend Unit** | Database connections, parsing APIs, RAG chunking logic | Pytest | `pytest backend/tests/` |
| **Frontend UI** | Component rendering, Zustand state updates | Vitest | `npm run test` (inside `frontend/`) |
| **End-to-End** | Complete user flows (e.g., Ingest -> Graph -> Code Build) | Playwright | `npx playwright test` |
| **Agentic QA** | Multi-agent output accuracy, prompt robustness | Custom Python runner | `python scripts/test_agents.py` |
| **Security** | PII filters, SQL injection vulnerabilities | Bandit / Custom checks | `bandit -r backend/app/` |

---

## 2. Agentic Regression & Prompt Quality Testing

Unlike deterministic software, testing AI agents requires evaluating statistical accuracy and formatting compliance over time.

- **Golden Dataset**: The repository contains a testing suite in `tests/golden_dataset.json` with 50 diverse seed ideas (e.g., "Build an offline password manager using SQLite").
- **Assertion Criteria**: For each execution run, the test validates:
  1. **Schema Compliance**: The output parses to the correct Pydantic structure without throwing exceptions.
  2. **Hallucination Check**: The output does not contain generic links (e.g. `example.com` or imaginary Github paths).
  3. **Performance Score**: Time to first token (TTFT) and overall execution duration remain within acceptable boundaries.

```python
# backend/tests/test_agents.py
import pytest
from app.agents.roles.research import ResearchAgent
from app.agents.schemas import ResearchOutputSchema

@pytest.mark.asyncio
async def test_research_agent_structured_output():
    # Setup test agent with mock LLM
    agent = ResearchAgent(model="mock-gemma")
    raw_idea = "A local-first encrypted markdown notebook application."
    
    # Run analysis
    result = await agent.analyze_idea(raw_idea)
    
    # Verify result fits our Pydantic schema
    assert isinstance(result, ResearchOutputSchema)
    assert len(result.required_skills) > 0
    assert result.suggested_license in ["MIT", "Apache-2.0", "GPL-3.0", "AGPL-3.0"]
    # Check that it doesn't include hallucinated links
    for competitor in result.competitor_list:
        assert competitor.url.startswith("http")
```

---

## 3. End-to-End Testing (Playwright)

We use Playwright to simulate user interactions on the UI, validating that state updates trigger mutations correctly.

```typescript
// frontend/e2e/workspace.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Workspace Navigation Flow', () => {
  test('should create a new project and view the graph', async ({ page }) => {
    // Navigate to local workspace dashboard
    await page.goto('http://localhost:5173');
    
    // Open Command Palette
    await page.keyboard.press('Control+P');
    await expect(page.locator('#command-palette')).toBeVisible();
    
    // Type and submit new project creation
    await page.type('#command-input', 'New SaaS Platform');
    await page.keyboard.press('Enter');
    
    // Verify redirection to Graph View
    await expect(page).toHaveURL(/.*\/graph/);
    
    // Ensure graph canvas has rendered
    const canvas = page.locator('#graph-canvas-main');
    await expect(canvas).toBeVisible();
  });
});
```
