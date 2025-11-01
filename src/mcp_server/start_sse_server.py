import logging

from src.mcp_server.tool_server import server_gx

if __name__ == '__main__':
    server_gx.run(
        transport= "sse",
        host="127.0.0.1",
        port=8180,
        log_level='debug',
        path = '/sse'
    )