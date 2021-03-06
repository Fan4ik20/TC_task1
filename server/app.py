from typing import Type

from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

from service import get_formatted_time, get_timezone


class DateHttpHandler(BaseHTTPRequestHandler):
    """
    This is a basic HttpRequest handler.
    In it, I have redefined the behaviour of the GET method
    so that it meets the condition of the assignment.

    """

    def _set_headers(self) -> None:
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _get_formatted_time(self) -> str:
        return get_formatted_time(get_timezone(self.client_address[0]))

    def _send_date(self) -> None:
        clients_time: str = self._get_formatted_time()

        if (clients_timezone := get_timezone(self.client_address[0])) is None:
            clients_timezone = (
                'Go to your computer date settings and look,'
                ' you are connected via local address'
            )

        self.wfile.write((
            f'Get connection from {self.client_address[0]}<br>'
            f'Your timezone is - {clients_timezone}<br>'
            f'Your time is - {clients_time}<br>'
        ).encode())

    def do_GET(self) -> None:
        self._set_headers()

        self._send_date()


class DateHttpServer:
    """Basic Http Server"""

    def __init__(
            self, host: str = '0.0.0.0', port: int = 65432,
            server: Type[HTTPServer] = HTTPServer,
            handler: Type[BaseHTTPRequestHandler] = DateHttpHandler
    ) -> None:
        self._host = host
        self._port = port
        self._handler = handler

        self._server = server((self._host, self._port), self._handler)

    def _log_meta_information(self) -> None:
        print('Author - Mark Zaianchkovskyi')
        print(f'Server was run in {datetime.now()}')
        print(f'Server is listening at port {self._port}')
        print(f'Server Host - {self._host}')

    def run_forever(self) -> None:
        self._log_meta_information()

        self._server.serve_forever()

    def close_server(self) -> None:
        self._server.server_close()


def main() -> None:
    server = DateHttpServer()

    server.run_forever()


if __name__ == '__main__':
    main()
