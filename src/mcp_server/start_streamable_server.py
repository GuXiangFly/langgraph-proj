import logging

from tool_server import server_gx

if __name__ == '__main__':
    server_gx.run(
        transport= "streamable-http",
        host="127.0.0.1",
        port=8181,
        log_level='debug',
        path = '/streamable'
    )