# backend/app/agents/orchestrator.py
import json
import logging
from app.config import settings
from app.agents.roles import AGENT_SYSTEM_PROMPTS, MOCK_RESPONSES, get_mock_response

# Conditional LiteLLM imports to prevent crash if not pre-installed
try:
    import litellm
except ImportError:
    litellm = None

logger = logging.getLogger("orchestrator")

class MultiAgentOrchestrator:
    def __init__(self):
        self.model = settings.LITELLM_MODEL
        self.enable_mock = settings.ENABLE_MOCK_AGENTS

    async def execute_agent_task(self, role: str, context_prompt: str) -> dict:
        """Dispatches prompts to specialized agent roles."""
        if role not in AGENT_SYSTEM_PROMPTS:
            raise ValueError(f"Unknown agent role: {role}")
            
        logger.info(f"Dispatching task to agent '{role}' using model '{self.model}'...")
        
        # 1. Fallback to mock logic if active or litellm missing
        if self.enable_mock or not litellm:
            logger.info("Mock Mode active. Returning predefined schema response.")
            return get_mock_response(role, context_prompt)
            
        # 2. Call real LLM using LiteLLM
        system_instruction = AGENT_SYSTEM_PROMPTS[role]
        try:
            # Construct standard message format
            messages = [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": context_prompt + "\n\nYou MUST reply with a single valid JSON payload matching the expected output fields."}
            ]
            
            # Call completion
            response = litellm.completion(
                model=self.model,
                messages=messages,
                api_base=settings.OLLAMA_API_BASE if "ollama" in self.model else None,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            # Parse json
            return json.loads(content)
        except Exception as e:
            logger.error(f"LiteLLM completion error: {e}. Falling back to mock data.")
            return MOCK_RESPONSES.get(role, {"error": str(e)})

    async def run_collaborative_debate(self, project_name: str, description: str) -> dict:
        """Simulates a multi-agent debate on project architecture and feasibility."""
        logger.info("Initializing multi-agent critique room...")
        
        # Run researcher and business models in parallel
        research = await self.execute_agent_task("researcher", f"Project: {project_name}. Description: {description}")
        business = await self.execute_agent_task("business", f"Project: {project_name}. Description: {description}")
        
        # Coder inputs critique based on developer complexity
        critique_prompt = f"Review this project: {project_name}. Research findings: {json.dumps(research)}. Business Model: {json.dumps(business)}"
        architect = await self.execute_agent_task("architect", critique_prompt)
        
        debate_result = {
            "project_name": project_name,
            "research_summary": research.get("summary"),
            "target_license": research.get("suggested_license"),
            "database_layout": architect.get("database_type"),
            "suggested_endpoints": architect.get("endpoints"),
            "monetization_plan": business.get("monetization"),
            "debate_transcript": [
                {"speaker": "Research Agent", "statement": "We verified key competitor gaps and recommend license: " + research.get("suggested_license", "MIT")},
                {"speaker": "Business Agent", "statement": "Our monetization forecast: " + business.get("monetization", "N/A")},
                {"speaker": "Architect Agent", "statement": "We mapped database configuration: " + architect.get("database_type", "SQLite")}
            ]
        }
        return debate_result

agent_orchestrator = MultiAgentOrchestrator()
