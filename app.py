from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)

app = Flask(__name__)
CORS(app, origins=['*'])

def crear_app():

    @app.route("/api/obtener-signos")
    def getSignos():
        url = "https://www.lavanguardia.com/horoscopo/signos-zodiaco"
        response = requests.get(url, verify=True)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            div_titulo = soup.find('h1', class_='section-title').text.strip()
            div_signos = soup.find('ul', class_='signs-grid').findAll('li', class_='zodiac-sign-item')

            lista_signos = []
            for element in div_signos:
                href_signo = element.find('a').get('href')
                img_signo = element.find('img').get('src')
                nombre_signo = element.find('h2').text.strip()
                fecha_signo = element.find('p').text.strip()
                lista_signos.append(
                    {
                        'href': href_signo,
                        'image': img_signo,
                        'name': nombre_signo,
                        'date': fecha_signo
                    }
                )

            return jsonify({'title': div_titulo, 'data': lista_signos})
        else:
            error = {'error': 'Ocurrio un error interno'}
            return jsonify(error)
    

    @app.route("/api/obtener-signo")
    def getSignoSolo():
        urlSigno = request.args.get('url-signo')
        url = "https://www.lavanguardia.com"+urlSigno+""
        response = requests.get(url, verify=True)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            img_signo = soup.find('div', class_='title-group').find('img').get('src')
            nombre_signo = soup.find('div', class_='sign-data').find('h1').text.strip()
            fecha_signo = soup.find('div', class_='sign-data').find('p').text.strip()
            parrafo_signo = soup.find('div', class_='text-block').find('p').text.strip()

            ul_links = soup.find('ul', class_='links').findAll('li')
            href_today = ul_links[-2].find('h2').find('a').get('href')
            href_manana = ul_links[-1].find('h2').find('a').get('href')

            return jsonify(
                {
                    'image': img_signo,
                    'name': nombre_signo,
                    'date': fecha_signo,
                    'content': parrafo_signo,
                    'href_today': href_today,
                    'href_tomorrow': href_manana
                }
            )
    
        else:
            error = {'error': 'Ocurrio un error interno'}
            return jsonify(error)
        
    return app

if __name__ == '__main__':
    app = crear_app()
    app.run()