# pycharai
CharacterAI wrapper for python. 

Usage
```python
# Must be you character_ai account credentials
email = 'example@gmail.com'
passwd = 'Passw0rd!"
char_id = '6HhWfeDjetnxESEcThlBQtEUo0O8YHcXyHqCgN7b2hY'
# https://beta.character.ai/chat?char=6HhWfeDjetnxESEcThlBQtEUo0O8YHcXyHqCgN7b2hY

ai = pyCharAI(char_id, email, passwd)

response = ai.ask('Can a butterfly dream?')

async def main(): # Also supports async operations
  response = await ai.ask_async('How should I improve this project?') 
  
asyncio.run(main())
```
 
