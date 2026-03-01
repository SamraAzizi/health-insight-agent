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

    def check_rate_limit(self):
        """Check if user has reached their analysis limit."""
        # Calculate time until reset
        time_until_reset = timedelta(days=1) - (datetime.now() - st.session_state.last_analysis)
        hours, remainder = divmod(time_until_reset.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        # Reset counter after 24 hours
        if time_until_reset.days < 0:
            st.session_state.analysis_count = 0
            st.session_state.last_analysis = datetime.now()
            return True, None
        
        # Check if limit reached
        if st.session_state.analysis_count >= st.session_state.analysis_limit:
            error_msg = f"Daily limit reached. Reset in {hours}h {minutes}m"
            return False, error_msg
        return True, None

    def analyze_report(self, data, system_prompt, check_only=False, chat_history=None):
        """
        Analyze report data using in-context learning from previous analyses.
        
        Args:
            data: Report data to analyze
            system_prompt: Base system prompt
            check_only: If True, only check rate limit without generating analysis
            chat_history: Previous messages in the current session (optional)
        """