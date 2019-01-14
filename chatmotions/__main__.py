import asyncio
import logging

from aiohttp import web

from chatmotions.app import create_app

logging.basicConfig(level=logging.INFO)


def main():
    # Create app
    app = create_app()

    web.run_app(app, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
