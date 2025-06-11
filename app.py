from flask import Flask, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Golden Result Tracker</title>
    <meta http-equiv="refresh" content="15" />
    <style>
        body { font-family: Arial; background: #111; color: #0f0; text-align: center; padding-top: 30px; }
        .result { font-size: 20px; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>📊 Golden Navratna Early Results</h1>
    {% for name, result in results.items() %}
        <div class="result">{{ name }}: {{ result }}</div>
    {% endfor %}
</body>
</html>
'''

def fetch_results():
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        driver.get("https://www.goldennavratnacoupon.com/results")
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        results = {}
        blocks = soup.find_all("div", class_="card-result")
        for block in blocks:
            game_name = block.find("h3")
            game_result = block.find("b") or block.find("span", class_="number")
            if game_name and game_result:
                results[game_name.text.strip()] = game_result.text.strip()

        return results if results else {"Error": "No results found"}

    except Exception as e:
        return {"Error": str(e)}

@app.route("/")
def index():
    results = fetch_results()
    return render_template_string(HTML_TEMPLATE, results=results)

if __name__ == "__main__":
    app.run()
    
