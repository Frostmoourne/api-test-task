import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from db_handler import db_handler


class HttpProcessor(BaseHTTPRequestHandler):
    """Сервер-обработчик GET-запросов"""
    print("Инициализация базы данных")
    api = db_handler()
    print("Инициализация базы данных завершена")

    def do_GET(self):
        # Парсим входящий url запрос
        sku = urlparse(self.path)
        # Запрашиваемый sku
        path = sku.path[1:]
        # Параметры url-запроса в виде словаря {'key': 'value'}
        query = parse_qs(sku.query)

        # Если такой sku присутствует в хранилище и запрос пришел с параметром
        if path in self.api and query:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            response = []
            try:
                for item in self.api[path]:
                    # Фильтр по значению параметра рекомендации
                    if float(item[1]) >= float(query['rate'][0]):
                        response.append(item)
                # Формирование json-ответа
                response = json.dumps({path: response[1:]})
                self.wfile.write(response.encode(encoding='utf-8'))
                
            except ValueError:
                print('Введите корректное значение параметра')
                self.wfile.write(b"Not Found")
            except KeyError:
                print('Введите корректное название параметра')
                self.wfile.write(b"Not Found")

        # Обработка ответа без параметра
        elif path in self.api:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            response = json.dumps({path: self.api[path]})
            self.wfile.write(response.encode(encoding='utf-8'))
        # Недействительный запрос
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Not Found")


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), HttpProcessor)
    server.serve_forever()
    print('End')
