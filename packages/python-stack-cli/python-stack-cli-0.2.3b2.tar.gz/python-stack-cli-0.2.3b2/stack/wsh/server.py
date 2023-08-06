# coding utf8


from aiohttp import web
from typing import Callable
from functools import partial
from ..utils import io_echo
from io import StringIO
import sys


def out(s: str):
    '''
    Show info message with yellow color
    '''
    return io_echo("\033[92mOut: {}\033[00m" .format(s))


def command_parser(cmd: str, fns: dict) -> Callable:
    '''
    get target function from funs dict and \
    map command like "cmd arg0 arg1 arg2 --key1=v1 --key2=v2" to \
    partial(fn, arg0, arg1, arg2, key1=v1, key2=v2)

    '''
    args = cmd.strip().split(' ')
    fn_name = args[0]
    args = [i for i in args[1:] if not i.startswith('-')]
    kwargs = dict([i.replace('-', '').split('=') for i in args[1:] if i.startswith('-')])
    return partial(fns.get(fn_name, lambda: 'None'), *args, **kwargs)


def io_wrapper(fn: Callable, ws: web.WebSocketResponse) -> str:
    io = StringIO()
    sys.stdout = sys.stderr = io
    res = fn() or io.getvalue()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    ws.send_str(out(res))
    io.close()
    del io
    return res


async def wsh(request, handler=print, project='default'):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        if msg.tp == web.MsgType.text:
            io_wrapper(handler(msg.data), ws)
        elif msg.tp == web.MsgType.binary:
            ws.send_bytes(msg.data)
        elif msg.tp == web.MsgType.close:
            print('websocket connection closed')
    return ws


def main(host='127.0.0.1', port='8964', pattern={}, project='default'):
    app = web.Application()
    app.router.add_route('GET', '/wsh/{project}', partial(wsh, project=project, handler=partial(command_parser, fns=pattern)))
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
