# Weather Agent 🌤️

A lightweight CLI weather assistant built with Python and the Groq SDK. It uses LLM tool calling to fetch real-time weather data and delivers the forecast with a TV weather reporter persona.

## Features
- **LLM Tool Calling:** Automatically detects when a user query requires live weather data and invokes a custom Python function.
- **Real-Time Weather:** Fetches current conditions and temperature using the `wttr.in` API (no weather API key required).
- **Custom Persona:** Delivers forecasts with practical, condition-based advice.
