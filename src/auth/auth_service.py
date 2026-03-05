import streamlit as st
from supabase import create_client
from datetime import datetime
import time
import re


class AuthService:
    def __init__(self):
        try:
            # Initialize Supabase client directly
            # This ensures a fresh client for each session, preventing state leakage
            self.supabase = create_client(
                st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"]
            )
        except Exception as e:
            st.error(f"Failed to initialize services: {str(e)}")
            raise e

        # Try to restore session from Supabase if no current session
        self.try_restore_session()

        # Validate session on initialization
        if "auth_token" in st.session_state:
            if not self.validate_session_token():
                # Don't sign out immediately on failure during init to avoid loop
                pass

    def try_restore_session(self):
        """Try to restore session from Supabase stored session."""
        try:
            # First try to restore from Streamlit session state tokens
            if "auth_token" in st.session_state and "refresh_token" in st.session_state:
                try:
                    self.supabase.auth.set_session(
                        st.session_state.auth_token, st.session_state.refresh_token
                    )
                except Exception as e:
                    # print(f"Set session failed: {e}")
                    pass

            # Check if Supabase has a stored session
            session = self.supabase.auth.get_session()
            if session and session.access_token:
                # If we have a session but it's not in state, restore it
                # Or if the token in state is stale/different, update it
                current_token = st.session_state.get("auth_token")
                if not current_token or current_token != session.access_token:
                    user = self.supabase.auth.get_user()
                    if user and user.user:
                        user_data = self.get_user_data(user.user.id)
                        if user_data:
                            st.session_state.auth_token = session.access_token
                            st.session_state.refresh_token = session.refresh_token
                            st.session_state.user = user_data