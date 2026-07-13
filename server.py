from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse


class MyServer(BaseHTTPRequestHandler):

    # Задание 2: Обработка ЛЮБОГО GET-запроса
    def do_GET(self):
        # Если браузер просит иконку вкладки (favicon), сразу говорим "нет", чтобы не вешать сервер
        if self.path == '/favicon.ico':
            self.send_response(404)
            self.end_headers()
            return

        try:
            # Читаем файл Контакты с помощью контекстного менеджера
            with open("catalog/contacts.html", "r", encoding="utf-8") as f:
                html_content = f.read()

            # Отправляем успешный статус ответа 200 OK
            self.send_response(200)

            # Изменяем заголовок на text/html по условию задания
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()  # Обязательно закрываем заголовки, чтобы браузер понял: пора читать данные!

            # Отправляем содержимое HTML-файла
            self.wfile.write(bytes(html_content, "utf-8"))

        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                bytes("Файл contacts.html не найден. Проверьте путь.", "utf-8"))

    # Дополнительное задание *: Прием POST-запроса от формы
    def do_POST(self):
        # 1. Определяем длину (размер) пришедших данных
        content_length = int(self.headers['Content-Length'])

        # 2. Считываем данные из потока и декодируем их в строку
        post_data = self.rfile.read(content_length).decode('utf-8')

        # 3. Декодируем строку формы (name=Ivan&email=test%40mail.ru) в словарь Python
        parsed_data = urllib.parse.parse_qs(post_data)

        # 4. Печать в консоль всех принятых от пользователя данных
        print("\n========================================")
        print("🔥 ПОЛУЧЕНЫ ДАННЫЕ ИЗ ФОРМЫ ОБРАТНОЙ СВЯЗИ:")
        for key, value in parsed_data.items():
            # Извлекаем значение из списка, так как parse_qs возвращает списки
            print(f"👉 {key}: {value[0]}")
        print("========================================\n")

        # Отправляем пользователю ответ об успешной отправке
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        response_html = """
        <html>
        <head><link href="https://jsdelivr.net" rel="stylesheet"></head>
        <body class="bg-light d-flex align-items-center justify-content-center vh-100">
            <div class="text-center p-5 bg-white rounded shadow">
                <h2 class="text-success mb-3">Успешно!</h2>
                <p class="text-muted">Ваше сообщение отправлено. Данные напечатаны в консоли PyCharm.</p>
                <a href="/" class="btn btn-primary mt-3">Назад к контактам</a>
            </div>
        </body>
        </html>
        """
        self.wfile.write(bytes(response_html, "utf-8"))


if __name__ == "__main__":
    # Запускаем локальный веб-сервер на порту 8000
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyServer)
    print("🚀 Сервер успешно запущен!")
    print("👉 Откройте в браузере: http://localhost:8000")
    httpd.serve_forever()