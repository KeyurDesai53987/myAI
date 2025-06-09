import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model_logic import get_model_format


def test_get_model_format_tinyllama():
    expected = {
        "chat_format": "chatml",
        "stop": ["<|user|>", "<|system|>", "<|assistant|>", "</s>"],
        "prefix_template": "<|system|>{system_prompt}</s><|user|>{user_input}</s><|assistant|>"
    }
    assert get_model_format("some/path/tinyllama-model") == expected


def test_get_model_format_mistral():
    expected = {
        "chat_format": "llama-2",
        "stop": ["You:", "Assistant:"],
        "prefix_template": "{system_prompt}\n\n{history}You: {user_input}\n{assistant_name}:"
    }
    assert get_model_format("model/mistral-7b") == expected


def test_get_model_format_phi():
    expected = {
        "chat_format": "prompt-style",
        "stop": ["User:", "Assistant:"],
        "prefix_template": "{system_prompt}\n\nUser: {user_input}\nAssistant:"
    }
    assert get_model_format("another/path/phi-2") == expected


def test_get_model_format_default():
    expected = {
        "chat_format": "plain",
        "stop": ["\n"],
        "prefix_template": "{system_prompt}\n\n{history}{user_input}"
    }
    assert get_model_format("some/other/model") == expected
