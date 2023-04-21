<h1 style="text-align: center">aio-spamwatch</h1>

<div style="text-align:center;">
  <a href="https://pypi.org/project/aio-spamwatch/" target="_blank">
    <img src="https://img.shields.io/pypi/v/aio-spamwatch.svg" alt="PyPI version">
  </a>
  <a href="https://github.com/NachABR/aio-spamwatch/blob/master/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/NachABR/aio-spamwatch.svg" alt="License">
  </a>
  <a href="https://github.com/psf/black" target="_blank">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
  </a>
</div>


An asynchronous Python wrapper for the [SpamWatch API](https://spamwat.ch/).

## Installation

```bash
pip install aio-spamwatch
```

## Usage
```python
import asyncio
from aio_spamwatch import SpamwatchAPI

client = SpamwatchAPI(token="TOKEN_HERE")


async def main():
    # import aiohttp
    # client = SpamwatchAPI(token="TOKEN_HERE", session=aiohttp.ClientSession())
    version = await client.version()
    print(version)


asyncio.run(main())
```


