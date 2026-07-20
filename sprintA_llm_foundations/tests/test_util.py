from groq_client import trim_history

def test_trim_history_keep_system_messages():
    messages = [{"role": "system", "content": "system_msg"}] + [{"role": "user", "content": f"msg{i}"} for i in range(20)]
    trimmed = trim_history(messages= messages, max_turns=3)
    assert trimmed[0] == {"role": "system", "content": "system_msg"}

def test_trim_history_respects_max_turns():
    messages = [{"role": "system", "content": "sys"}]
    for i in range(10):
        messages.append({"role": "user", "content": f"u{i}"})
        messages.append({"role": "assistant", "content": f"a{i}"})

    trimmed = trim_history(messages=messages, max_turns=3)
    assert len(trimmed) == 7

def test_trim_history_under_limit_unchanged():
    messages = [{"role": "system", "content": "sys"}, {"role": "user", "content": "hi"}]
    assert trim_history(messages= messages, max_turns=5) == messages
