def trim_history(messages: list[dict], max_turns:int) -> list[dict]:
    """Keep only the system message plus only the most recent max_turn user assistant pairs"""
    system_messages: list[dict] = [m for m in messages if m["role"] == "system"]
    conversations: list[dict] = [m for m in messages if m["role"] != "system"]
    trimmed_conversations: list[dict] = conversations[-(max_turns * 2):]
    return system_messages + trimmed_conversations