from typing import Type

from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

from service import get_formatted_time, get_timezone


class DateHttpHandler(BaseHTTPRequestHandler):
    def _set_headers(self) -> None:
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _get_formatted_time(self) -> str:
        # If local address == request address.
        if self.server.server_address[0] == self.client_address[0]:
            return datetime.now().strftime("%d:%m:%Y %H:%M:%S")

        return get_formatted_time(get_timezone(self.client_address[0]))

    def _send_date(self) -> None:
        clients_date: str = self._get_formatted_time()

        self.wfile.write((
            f'Get connection from {self.client_address[0]}<br>'
            f'Your time is - {clients_date}<br>'
        ).encode())

    def do_GET(self) -> None:
        self._set_headers()

        self._send_date()


class DateHttpServer:
    def __init__(
            self, host: str = 'localhost', port: int = 65432,
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
