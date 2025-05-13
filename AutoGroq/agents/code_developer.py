# agents/code_developer.py

import datetime
import streamlit as st
from configs.config import LLM_PROVIDER
from models.agent_base_model import AgentBaseModel
from models.tool_base_model import ToolBaseModel
from tools.code_generator import code_generator_tool

class CodeDeveloperAgent(AgentBaseModel):
    def __init__(self, name, description, tools, config, role, goal, backstory, provider, model):
        current_timestamp = datetime.datetime.now().isoformat()
        super().__init__(name=name, description=description, tools=tools, config=config,
                         role=role, goal=goal, backstory=backstory)
        self.provider = provider
        self.model = model
        self.created_at = current_timestamp
        self.updated_at = current_timestamp
        self.user_id = "default"
        self.timestamp = current_timestamp

    @classmethod
    def create_default(cls):
        return cls(
            name="Code Developer",
            description="An agent specialized in generating code based on feature descriptions.",
            tools=[code_generator_tool],
            config={
                "llm_config": {
                    "config_list": [{"model": st.session_state.get('model', 'default'), "api_key": None}],
                    "temperature": st.session_state.get('temperature', 0.7)
                },
                "human_input_mode": "NEVER",
                "max_consecutive_auto_reply": 10
            },
            role="Code Developer",
            goal="To create efficient and effective code solutions based on given requirements.",
            backstory="I am an AI agent with extensive knowledge of various programming languages and software development best practices. My purpose is to assist in creating code that meets the specified requirements.",
            provider=st.session_state.get('provider', LLM_PROVIDER),
            model=st.session_state.get('model', 'default')
        )
    

    def to_dict(self):
        def make_serializable(obj):
            if isinstance(obj, (str, int, float, bool, type(None))):
                return obj
            elif isinstance(obj, dict):
                return {k: make_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple, set)):
                return [make_serializable(v) for v in obj]
            elif hasattr(obj, "to_dict"):
                return obj.to_dict()
            elif hasattr(obj, "__dict__"):
                # Avoid recursion on self
                if obj is self:
                    return None
                return make_serializable(obj.__dict__)
            else:
                return str(obj)  # fallback to string representation

        data = {}
        for key, value in self.__dict__.items():
            # Exclude callables and modules
            if callable(value) or key.startswith("__"):
                continue
            data[key] = make_serializable(value)
        return data