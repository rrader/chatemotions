import logging

from aiohttp import web

from chatmotions.chat import get_chat

from chatmotions.sentiment import init_dostoevsky

log = logging.getLogger(__name__)


def create_app():
    init_dostoevsky()

    # Create app
    app = web.Application()

    # Routes
    app.router.add_get('/health', health_check)
    app.router.add_post('/message/{chat_id}', message)
    app.router.add_get('/status/{chat_id}', chat_status)
    app.router.add_post('/reset_should_respond/{chat_id}', reset_should_respond)

    return app


async def health_check(request):
    return web.json_response({'status': 'ok'}, status=200)


async def message(request):
    chat_id = request.match_info['chat_id']
    chat = get_chat(chat_id)

    data = await request.json()
    chat.message_posted(**data)
    return web.json_response({
        'status': 'ok'
    }, status=200)


async def chat_status(request):
    chat_id = request.match_info['chat_id']
    chat = get_chat(chat_id)

    respond = chat.should_respond()
    return web.json_response({
        'shouldRespond': respond
    }, status=200)


async def reset_should_respond(request):
    chat_id = request.match_info['chat_id']
    chat = get_chat(chat_id)

    chat.reset_polarity()
    return web.json_response({
        'status': 'ok'
    }, status=200)
