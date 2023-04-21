<h1 assign="center">aio-spamwatch<h1>

[![PyPI version](https://img.shields.io/pypi/v/aio-spamwatch.svg)](https://pypi.org/project/aio-spamwatch/)
[![License](https://img.shields.io/github/license/NachABR/aio-spamwatch.svg)](https://github.com/NachABR/aio-spamwatch/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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


