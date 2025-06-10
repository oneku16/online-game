import pytest
from httpx import AsyncClient


class TestTournament:

    @pytest.mark.asyncio
    async def test_create_tournament(self, client: AsyncClient) -> None:
        tournament_data = {
            "name": "Mock Tournament",
            "max_players": 2,
            "start_date": "2025-06-01T15:00:00Z",
        }

        response = await client.post(
            url="/game/tournaments",
            json=tournament_data,
        )
        print(f"{response=}")

        assert response.status_code == 200
        response = response.json()
        assert response["name"] == tournament_data["name"]
        assert response["max_players"] == tournament_data["max_players"]

    @pytest.mark.asyncio
    async def test_player_registration(self, client: AsyncClient) -> None:
        tournament_response = await client.post(
            url="/game/tournaments",
            json={
                "name": "Mock Tournament 2",
                "max_players": 1,
                "start_date": "2025-06-01T15:00:00Z",
            },
        )
        assert tournament_response.status_code == 200

        response = await client.post(
            url=f"/game/tournaments/{tournament_response.json()["id"]}/register?name=Eku&email=eku@eku.com"
        )
        assert response.status_code == 200
        response = response.json()
        assert response["name"] == "Mock Tournament 2"
        assert response["id"] == tournament_response.json()["id"]

    @pytest.mark.asyncio
    async def test_duplicate_email_fails(self, client: AsyncClient) -> None:
        tournament_response = await client.post(
            url="/game/tournaments",
            json={
                "name": "Mock Tournament 2",
                "max_players": 2,
                "start_date": "2025-06-01T15:00:00Z",
            },
        )
        assert tournament_response.status_code == 200

        # 1st registration (success)
        response1 = await client.post(
            url="/game/tournaments/1/register?name=Eku&email=eku@eku.com"
        )
        assert response1.status_code == 200

        # 2nd registration (should fail)
        response2 = await client.post(
            url="/game/tournaments/1/register?name=Eku&email=eku@eku.com"
        )

        assert response2.status_code == 400
        assert "already registered" in response2.json()["detail"]

    @pytest.mark.asyncio
    async def test_player_registration_no_slots(self, client: AsyncClient) -> None:
        tournament_response = await client.post(
            url="/game/tournaments",
            json={
                "name": "Mock Tournament 3",
                "max_players": 1,
                "start_date": "2025-06-01T15:00:00Z",
            },
        )
        assert tournament_response.status_code == 200

        # 1st reg (success)
        response1 = await client.post(
            url="/game/tournaments/1/register?name=Eku&email=eku@eku.com"
        )
        assert response1.status_code == 200

        # 2d reg (should fail)
        response2 = await client.post(
            url="/game/tournaments/1/register?name=Eku&email=eku@eku.org"
        )

        assert response2.status_code == 400
        assert "no empty slots" in response2.json()["detail"]
