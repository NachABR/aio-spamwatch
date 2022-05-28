"""Client class for the Wrapper."""
from json import JSONDecodeError
from typing import Dict, List, Tuple, Union, Any, Optional

import asyncio

import aiohttp
from aiohttp import ClientResponse

from .errors import Error, Forbidden, NotFoundError, UnauthorizedError, TooManyRequests
from .types import Ban, Permission, Token


class Client:
    """Client to interface with the SpamWatch API."""

    def __init__(self,
                token: str,
                *,
                host: str = 'https://api.spamwat.ch',
                loop: Optional[asyncio.AbstractEventLoop] = None
                ) -> None:
        """
        Args:
            token: The Authorization Token
            host: The API host. Defaults to the official API.
        """
        self._host = host
        self._kk = token
        self._session = None
        if not loop:
            try:
                self._loop = asyncio.get_running_loop()
            except RuntimeError:
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)
        

    def __del__(self):
        try:
            loop = asyncio.get_running_loop()
            asyncio.create_task(self._close_session())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self._close_session())

    async def _close_session(self):
        if not self._session.closed:
            await self._session.close()

    async def _make_request(self,
                            path: str,
                            method: str = 'get',
                            **kwargs: Dict[Any, Any]
                            ) -> Any:
        """
        Make a request and handle errors

        Args:
            path: Path on the API without a leading slash
            method: The request method. Defaults to GET
            **kwargs: Keyword arguments passed to the request method.

        Returns: The json response

        """
        if not self._session:
            self._session = aiohttp.ClientSession()
            self._session.headers.update({"Authorization": f"Bearer {self._kk}"})
            self._token = await self.get_self()
            self.permission = self._token.permission

        req = await self._session._request(method=method.upper(), str_or_url=f'{self._host}/{path}',
                                          **kwargs)
        if req.status in [200, 201]:
            try:
                return (await req.json())
            except JSONDecodeError:
                return (await req.text())
        if req.status == 204:
            return {}
        elif req.status == 401:
            raise UnauthorizedError("Make sure your Token is correct")
        elif req.status == 403:
            raise Forbidden(self._token)
        elif req.status == 404:
            raise NotFoundError()
        elif req.status == 429:
            raise TooManyRequests(path, (await req.json()).get('until', 0))
        else:
            raise Error(req)

    async def version(self) -> Dict[str, str]:
        """Get the API version"""
        return (await self._make_request('version'))

    # region Tokens
    async def get_tokens(self) -> List[Token]:
        """Get all tokens
        Requires Root permission

        Returns: A list of Tokens

        """
        data = await self._make_request('tokens')
        return [Token(**token) for token in data]

    async def create_token(self, userid: int, permission: Permission) -> Token:
        """Creates a token with the given parameters
        Requires Root permission

        Args:
            userid: The Telegram User ID of the token owner
            permission: The permission level the Token should have

        Returns: The created Token

        """
        data = await self._make_request('tokens', method='post',
                                             json={"id": userid,
                                                   "permission": permission.name})
        return Token(**data)

    async def get_self(self) -> Token:
        """Gets the Token that the request was made with."""
        data = await self._make_request('tokens/self')
        return Token(**data)

    async def get_token(self, token_id: int) -> Token:
        """Get a token using its ID
        Requires Root permission

        Args:
            token_id: The token ID

        Returns: The token

        """
        data = await self._make_request(f'tokens/{token_id}')
        return Token(**data)

    async def delete_token(self, token_id: int) -> None:
        """Delete a token using its ID

        Args:
            token_id: The id of the token

        """
        await self._make_request(f'tokens/{token_id}', method='delete')

    # endregion

    # region Bans
    async def get_bans(self) -> List[Ban]:
        """Get a list of all bans
        Requires Admin Permission

        Returns: A list of Bans

        """
        data = await self._make_request('banlist')
        return [Ban(**ban) for ban in data]

    async def get_bans_min(self) -> List[int]:
        data = await self._make_request('banlist/all')

        if data:
            if isinstance(data, int):
                return [data]
            else:
                return [int(uid) for uid in data.split('\n')]
        else:
            return []

    async def add_ban(self, user_id: int, reason: str, message: Optional[str] = None) -> None:
        """Adds a ban

        Args:
            user_id: ID of the banned user
            reason: Reason why the user was banned
        """
        ban = {
            "id": user_id,
            "reason": reason
        }
        if message:
            ban["message"] = message
        await self._make_request('banlist', method='post',
                                 json=[ban])

    async def add_bans(self, data: List[Ban]) -> None:
        """Add a list of Bans

        Args:
            data: List of Ban objects
        """
        _data = [{"id": d.id, "reason": d.reason} for d in data]
        await self._make_request('banlist', method='post',
                                 json=_data)

    async def get_ban(self, user_id: int) -> Union[Ban, bool]:
        """Gets a ban

        Args:
            user_id: ID of the user

        Returns: Ban object or None

        """
        try:
            data = await self._make_request(f'banlist/{user_id}')
            return Ban(**data)
        except NotFoundError:
            return False

    async def delete_ban(self, user_id: int) -> None:
        """Remove a ban"""
        await self._make_request(f'banlist/{user_id}', method='delete')

    # endregion

    # region Stats
    async def stats(self) -> Dict[str, int]:
        """Get ban stats"""
        data = await self._make_request('stats')
        return data
    # endregion
