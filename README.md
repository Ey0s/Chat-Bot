# Chat-Ey Bot v2.0.0

Chat-Ey Bot is now organized as a cleaner, modular Python app with better intent matching, safer history persistence, and a scalable folder structure.

## What Improved In 2.0.0
1. Better project organization with a src-based package layout.
2. Improved response quality using token overlap plus fuzzy matching.
3. Dynamic response templates for date and time.
4. More reliable history persistence in a dedicated data directory.
5. Backward compatibility launcher through chat.py.

## Folder Structure
```text
Chat-Bot/
  chat.py
  README.md
  requirements.txt
  responses.json
  data/
    responses.json
    history.json           # created automatically
  src/
    chatbot/
      __init__.py
      __main__.py
      app.py
      bot.py
      storage.py
      ui.py
```

## Run The App
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Start from the legacy launcher:
```bash
python chat.py
```

## How Response Matching Works
1. Dynamic intents are checked first (for date/time style requests).
2. Static and extended categories are scored using:
   - direct phrase containment,
   - token overlap,
   - fuzzy similarity.
3. If confidence is below threshold, the default fallback response is used.

## Your Data Files
1. Primary response dataset is in data/responses.json.
2. Legacy fallback file remains responses.json.
3. Conversation history is saved to data/history.json.

## Best Thoughts For Next Upgrades
1. Add unit tests for matcher scoring in src/chatbot/bot.py.
2. Add a profile mode with user nickname and preferred tone.
3. Add lightweight command mode (for example: /help, /clear, /history).
4. Add export chat to txt and json from the UI.
5. Add optional small local LLM integration while keeping JSON fallback.

## Version
Current version: 2.0.0

Created by Eyosyas.
