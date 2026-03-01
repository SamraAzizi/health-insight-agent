from datetime import datetime, timedelta
import streamlit as st
from agents.model_manager import ModelManager

class AnalysisAgent:
    """
    Agent responsible for managing report analysis, rate limiting,
    and implementing in-context learning from previous analyses.
    """
    
    def __init__(self):
        self.model_manager = ModelManager()
        self._init_state()
        
    def _init_state(self):
        """Initialize analysis-related session state variables."""
        if 'analysis_count' not in st.session_state:
            st.session_state.analysis_count = 0
        if 'last_analysis' not in st.session_state:
            st.session_state.last_analysis = datetime.now()
        if 'analysis_limit' not in st.session_state:
            st.session_state.analysis_limit = 15
        if 'models_used' not in st.session_state:
            st.session_state.models_used = {}
        if 'knowledge_base' not in st.session_state:
            st.session_state.knowledge_base = {}