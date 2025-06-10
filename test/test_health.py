import pytest
from httpx import AsyncClient


class TestHealthCheck:

    @pytest.mark.asyncio
    async def test_dummy(self, client: AsyncClient) -> None:
        res = await client.get("/")
        assert res.status_code in [200, 404]
