"""Fixtures for KB generator tests."""
import os


def pytest_configure():
    os.environ["OPENAI_API_KEY"] = "mocked_value"
