"""Client class for the Wrapper."""
from typing import Dict, List, Union, Optional

import aiohttp
from .errors import (
    APIError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    TooManyRequestsError,
)
from .types import Ban, Permission, Token


class SpamWatchAPI:
    def __init__(self, token: str, session: Optional[aiohttp.ClientSession] = None):
        self._token = token
        self._session = session
        self._base_url = "https://api.spamwat.ch"

    async def _make_request(self, path: str, method: str = "get") -> dict:
        async with self._session or aiohttp.ClientSession() as session:
            async with session.request(
                method=method.upper(),
                url=f"{self._base_url}/{path}",
                headers={"Authorization": f"Bearer {self._token}"},
            ) as request:
                if request.status == 200:
                    return await request.json()
                if request.status == 204:
                    return {}
                if request.status > 400:
                    if request.status == 401:
                        raise UnauthorizedError(
                            message="Make sure your token is correct.", url=request.url
                        )
                    elif request.status == 403:
                        raise ForbiddenError(
                            token=await self.get_self(), url=request.url
                        )
                    elif request.status == 404:
                        raise NotFoundError(message="", url=request.url)
                    elif request.status == 429:
                        raise TooManyRequestsError(
                            method=path,
                            until=(await request.json()).get("until", 0),
                            url=request.url,
                        )
                    else:
                        raise APIError(
                            code=request.status,
                            message=await request.text(),
                            url=request.url,
                        )

    # region Version
    async def version(self) -> Dict[str, str]:
        """Get the API version"""
        return await self._make_request(path="version")

    # endregion

    # region Tokens
    async def get_self(self) -> Token:
        """Gets the Token that the request was made with."""
        token = await self._make_request(path="tokens/self")
        return Token(**token)

    async def get_tokens(self) -> List[Token]:
        """Get all tokens
        Requires Root permission

        Returns: A list of Tokens

        """
        tokens = await self._make_request(path="tokens")
        return [Token(**token) for token in tokens]

    async def create_token(self, user_id: int, permission: Permission) -> Token:
        """Creates a token with the given parameters
        Requires Root permission

        Args:
            user_id: The Telegram User ID of the token owner
            permission: The permission level the Token should have

        Returns: The created Token

        """
        token = await self._make_request(
            path="tokens",
            method="post",
            json={"id": user_id, "permission": permission.name},
        )
        return Token(**token)

    async def get_token(self, token_id: int) -> Token:
        """Get a token using its ID
        Requires Root permission

        Args:
            token_id: The token ID

        Returns: The token

        """
        token = await self._make_request(path=f"tokens/{token_id}")
        return Token(**token)

    async def delete_token(self, token_id: int) -> None:
        """Delete a token using its ID

        Args:
            token_id: The id of the token

        """
        await self._make_request(path=f"tokens/{token_id}", method="delete")

    # endregion

    # region Bans
    async def get_bans(self) -> List[Ban]:
        """Get a list of all bans
        Requires Admin Permission

        Returns: A list of Bans

        """
        banlist = await self._make_request(path="banlist")
        return [Ban(**ban) for ban in banlist]

    async def get_bans_min(self) -> List[int]:
        banlist = await self._make_request(path="banlist/all")

        if not banlist:
            return []
        if isinstance(banlist, int):
            return [banlist]
        else:
            return [int(uid) for uid in banlist.split("\n")]

    async def add_ban(
        self, user_id: int, reason: str, message: Optional[str] = None
    ) -> None:
        """Adds a ban

        Args:
            user_id: ID of the banned user
            reason: Reason why the user was banned
        """
        ban = {"id": user_id, "reason": reason}
        if message:
            ban["message"] = message
        await self._make_request(path="banlist", method="post", json=[ban])

    async def add_bans(self, banlist: List[Ban]) -> None:
        """Add a list of Bans

        Args:
            data: List of Ban objects
        """
        banlist = [{"id": banned.id, "reason": banned.reason} for banned in banlist]
        await self._make_request(path="banlist", method="post", json=banlist)

    async def get_ban(self, user_id: int) -> Union[Ban, bool]:
        """Gets a ban

        Args:
            user_id: ID of the user

        Returns: Ban object or None

        """
        try:
            banned = await self._make_request(path=f"banlist/{user_id}")
            return Ban(**banned)
        except NotFoundError:
            return False

    async def delete_ban(self, user_id: int) -> None:
        """Remove a ban"""
        await self._make_request(path=f"banlist/{user_id}", method="delete")

    # endregion

    # region Stats
    async def stats(self) -> Dict[str, int]:
        """Get ban stats"""
        return await self._make_request(path="stats")

    # endregion
