"""
This module defines pre-configured AI agent modes available in the BlackboxAPI.
Each agent is specialized for specific tasks and conversation styles.
"""

from typing import Dict
from .models import AgentMode

# Agent mode descriptions
AGENT_DESCRIPTIONS: Dict[str, str] = {
    "PROMPT_GENERATOR": "Specialized in creating optimized prompts for various AI models and use cases",
    "RU_CAN_CODER": "Russian-speaking coding assistant with expertise in multiple programming languages",
    "RU_RELATIONSHIP_COACH": "Russian-speaking relationship advisor offering personal guidance",
    "RU_MENTAL_ADVISOR": "Russian-speaking mental health advisor providing supportive guidance",
    "RU_ALGORITHM_EXPLAINER": "Russian-speaking expert in explaining algorithms and computational concepts",
    "RU_IT_EXPERT": "Russian-speaking IT professional with broad technical knowledge",
    "RU_MATH_TEACHER": "Russian-speaking mathematics teacher for educational support",
    "RU_MATH_EXPERT": "Russian-speaking advanced mathematics expert for complex problems"
}

# Pre-configured agent modes
PROMPT_GENERATOR = AgentMode(
    mode=False,
    id="PromptGeneratorwFvlqld",
    name="Prompt Generator",
    description=AGENT_DESCRIPTIONS["PROMPT_GENERATOR"]
)

RU_CAN_CODER = AgentMode(
    mode=True,
    id="CANCoderwFvlqld",
    name="CAN Coder",
    description=AGENT_DESCRIPTIONS["RU_CAN_CODER"]
)

RU_RELATIONSHIP_COACH = AgentMode(
    mode=True,
    id="RelationshipCoach2VKd7cI",
    name="Relationship Coach",
    description=AGENT_DESCRIPTIONS["RU_RELATIONSHIP_COACH"]
)

RU_MENTAL_ADVISOR = AgentMode(
    mode=True,
    id="MentalhealthadviserPVcINVP",
    name="Mental Advisor",
    description=AGENT_DESCRIPTIONS["RU_MENTAL_ADVISOR"]
)

RU_ALGORITHM_EXPLAINER = AgentMode(
    mode=True,
    id="AlghorithmExplainer8K0Wxup",
    name="Algorithm Explainer",
    description=AGENT_DESCRIPTIONS["RU_ALGORITHM_EXPLAINER"]
)

RU_IT_EXPERT = AgentMode(
    mode=True,
    id="ITExpertNj4P5jL",
    name="IT Expert",
    description=AGENT_DESCRIPTIONS["RU_IT_EXPERT"]
)

RU_MATH_TEACHER = AgentMode(
    mode=True,
    id="MathsteachertSzUGhE",
    name="Maths Teacher",
    description=AGENT_DESCRIPTIONS["RU_MATH_TEACHER"]
)

RU_MATH_EXPERT = AgentMode(
    mode=True,
    id="Mathexpertb2Vibf5",
    name="Math Expert",
    description=AGENT_DESCRIPTIONS["RU_MATH_EXPERT"]
)

# List of all available agents for easy access
AVAILABLE_AGENTS = [
    PROMPT_GENERATOR,
    RU_CAN_CODER,
    RU_RELATIONSHIP_COACH,
    RU_MENTAL_ADVISOR,
    RU_ALGORITHM_EXPLAINER,
    RU_IT_EXPERT,
    RU_MATH_TEACHER,
    RU_MATH_EXPERT
]

def get_agent_by_id(agent_id: str) -> AgentMode:
    """Retrieve an agent mode by its ID.
    
    Args:
        agent_id (str): The ID of the agent to retrieve
        
    Returns:
        AgentMode: The requested agent mode
        
    Raises:
        ValueError: If no agent with the given ID exists
    """
    for agent in AVAILABLE_AGENTS:
        if agent.id == agent_id:
            return agent
    raise ValueError(f"No agent found with ID: {agent_id}")

def get_agent_by_name(name: str) -> AgentMode:
    """Retrieve an agent mode by its name.
    
    Args:
        name (str): The name of the agent to retrieve
        
    Returns:
        AgentMode: The requested agent mode
        
    Raises:
        ValueError: If no agent with the given name exists
    """
    for agent in AVAILABLE_AGENTS:
        if agent.name.lower() == name.lower():
            return agent
    raise ValueError(f"No agent found with name: {name}")