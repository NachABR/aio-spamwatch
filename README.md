# Asyncio SpamWatch API Wrapper

## Basic Usage

```python
import asyncio
import aio_sw

token = 'A_LONG_TOKEN_HERE'
client = aio_sw.Client(token)

async def main():
    r = await client.version()
    print(r)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
