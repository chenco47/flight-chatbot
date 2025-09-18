#!/usr/bin/env python3
"""
Flight Company AI Chatbot
A conversational AI assistant for customer support.
"""

import openai
import os
from typing import List, Dict

class BaseOpenAI:
    """Base class for OpenAI implementations"""
    pass

class OpenAI(BaseOpenAI):
    """OpenAI LLM using BaseOpenAI Class.
    An API call to OpenAI API is sent and response is recorded and returned.
    The default chat model is **gpt-3.5-turbo**.
    The list of supported Chat models includes ["gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano", "gpt-4o", "gpt-4o-mini", "gpt-4", "gpt-4-0613", "gpt-4-32k",
     "gpt-4-32k-0613", "gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-0613",
     "gpt-3.5-turbo-16k-0613", "gpt-3.5-turbo-instruct"].
    The list of supported Completion models includes "gpt-3.5-turbo-instruct" and other legacy models.
    """

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """Initialize OpenAI client with API key and model."""
        openai.api_key = api_key
        self.model = model

class FlightChatbot:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.conversation_history: List[Dict[str, str]] = []

        # Conversational system prompt for customer-facing chatbot
        self.system_prompt = """You are a helpful customer service representative for SkyLine Airways.
        You assist customers with flight bookings, cancellations, schedule changes, baggage policies,
        and general travel inquiries. Be friendly, professional, and conversational. Always try to
        help the customer resolve their issues efficiently."""

    def chat(self, user_message: str) -> str:
        """Send message to GPT-3.5 and get response"""
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": user_message})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )

        assistant_message = response.choices[0].message.content

        # Store conversation
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": assistant_message})

        return assistant_message

def main():
    """Simple CLI interface for the chatbot"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY environment variable")
        return

    chatbot = FlightChatbot(api_key)
    print("SkyLine Airways Customer Support Chatbot")
    print("Type 'quit' to exit")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break

        response = chatbot.chat(user_input)
        print(f"Assistant: {response}")

if __name__ == "__main__":
    main()