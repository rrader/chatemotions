import datetime

from chatmotions.app import create_app
from chatmotions.chat import get_chat
from chatmotions.sentiment import sentiment_analysis


async def test_health(aiohttp_client, loop):
    app = create_app()

    client = await aiohttp_client(app)
    resp = await client.get('/health')
    assert resp.status == 200
    text = await resp.text()
    assert '{"status": "ok"}' in text
