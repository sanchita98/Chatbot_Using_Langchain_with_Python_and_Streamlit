import uuid  # For generating unique session IDs

class SessionManager:
    """
    Manages chat sessions and their conversation histories.
    Supports creating, renaming, saving, and retrieving sessions.
    """

    def __init__(self, sessions_dict=None):
        """
        Initialize the SessionManager.

        Args:
            sessions_dict (dict, optional): External dictionary to manage sessions 
                                            (e.g., Streamlit's session_state['sessions']).
                                            If not provided, a new internal dictionary is created.
        """
        # Use provided sessions dictionary or create a new one
        self.sessions = sessions_dict if sessions_dict is not None else {}

    def create_session(self, name=None):
        """
        Create a new session with a unique or custom name.

        Args:
            name (str, optional): Optional custom session name. 
                                  If not provided, a random session ID is generated.

        Returns:
            str: The session ID or name of the newly created session.
        """
        # Generate a unique session name if not provided
        session_id = name if name else f"session_{uuid.uuid4().hex[:6]}"
        # Initialize an empty conversation list for this session
        self.sessions[session_id] = []
        return session_id

    def rename_session(self, old_name, new_name):
        """
        Rename an existing session.

        Args:
            old_name (str): The current session name.
            new_name (str): The new name to assign.

        Returns:
            str: The updated session name if successful, otherwise the original name.
        """
        # Ensure old session exists and new name is not empty/whitespace
        if old_name in self.sessions and new_name.strip():
            # Move session data to new key (rename)
            self.sessions[new_name] = self.sessions.pop(old_name)
            return new_name
        return old_name

    def save_turn(self, session_id, role, message):
        """
        Save a single conversation turn (role + message) to a given session.

        Args:
            session_id (str): The ID/name of the session.
            role (str): The speaker role (e.g., "user" or "assistant").
            message (str): The message content to store.
        """
        # Create session entry if it doesn't exist
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        # Append new message to the session history
        self.sessions[session_id].append({"role": role, "content": message})
    
    def get_history(self, session_id):
        """
        Retrieve the full conversation history for a session.

        Args:
            session_id (str): The ID/name of the session.

        Returns:
            list: List of dictionaries containing the conversation history.
                  Each entry has {'role': ..., 'content': ...}.
        """
        return self.sessions.get(session_id, [])
