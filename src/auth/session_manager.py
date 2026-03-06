import streamlit as st
from datetime import datetime, timedelta
from config.app_config import SESSION_TIMEOUT_MINUTES
import json

class SessionManager:
    @staticmethod
    def init_session():
        """Initialize or validate session."""
        # Initialize session only once per browser session
        if 'session_initialized' not in st.session_state:
            st.session_state.session_initialized = True
            # Try to restore session from persistent storage
            SessionManager._restore_from_storage()
            
        if 'auth_service' not in st.session_state:
            from auth.auth_service import AuthService
            st.session_state.auth_service = AuthService()
        
        # Check session timeout
        if 'last_activity' in st.session_state:
            idle_time = datetime.now() - st.session_state.last_activity
            if idle_time > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
                SessionManager.clear_session_state()
                st.error("Session expired. Please log in again.")
                st.rerun()
        
        # Update last activity
        st.session_state.last_activity = datetime.now()
        
        # Validate token and user data
        if 'user' in st.session_state:
            user_data = st.session_state.auth_service.validate_session_token()
            if not user_data:
                SessionManager.clear_session_state()
                st.error("Invalid session. Please log in again.")
                st.rerun()
    
    @staticmethod
    def _restore_from_storage():
        """Restore session from persistent storage."""
        try:
            # Inject storage script to enable localStorage functionality
            SessionManager._inject_storage_script()
            
            # The actual restoration happens in AuthService.try_restore_session()
            # which uses Supabase's built-in session persistence
            
        except Exception:
            pass  # Ignore errors during restoration
    
    @staticmethod
    def _inject_storage_script():
        """Inject JavaScript for persistent storage management."""
        storage_script = """
        <script>
        // Check if user data exists in localStorage on page load
        window.addEventListener('DOMContentLoaded', function() {
            const storedAuth = localStorage.getItem('hia_auth');
            if (storedAuth) {
                try {
                    const authData = JSON.parse(storedAuth);
                    // Set a flag that Python can check
                    window.hia_auth_data = authData;
                } catch (e) {
                    localStorage.removeItem('hia_auth');
                }
            }
        });
        
        // Function to save auth data
        window.saveAuthData = function(authData) {
            localStorage.setItem('hia_auth', JSON.stringify(authData));
        };
        
        // Function to clear auth data
        window.clearAuthData = function() {
            localStorage.removeItem('hia_auth');
        };
        
        // Function to get auth data
        window.getAuthData = function() {
            const stored = localStorage.getItem('hia_auth');
            return stored ? JSON.parse(stored) : null;
        };
        </script>
        """
        st.markdown(storage_script, unsafe_allow_html=True)