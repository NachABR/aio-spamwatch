# SpamWatch API Python Wrapper

## Basic Usage

```python
import spamwatch
token = 'A_LONG_TOKEN_HERE'
client = spamwatch.Client(token)
ban = client.get_ban(777000)
print(ban.reason)
```

## Async

```python
import spamwatch
import asyncio
token = 'A_LONG_TOKEN_HERE'
client = spamwatch.aioClient(token)

async def main():
    r = await client.version()
    print(r)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
