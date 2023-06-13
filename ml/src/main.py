import argparse

import routers
import uvicorn
from fastapi import FastAPI

app = FastAPI()

app.include_router(routers.router)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=8080, type=int, dest='port')
    parser.add_argument('--host', default='0.0.0.0', type=str, dest='host')
    parser.add_argument('--debug', action='store_true', dest='debug')
    args = vars(parser.parse_args())

    if args.get('debug'):
        uvicorn.run(
            'main:app', host=args['host'], port=args['port'], reload=True
        )
    else:
        uvicorn.run(
            'main:app', host=args['host'], port=args['port']
        )
