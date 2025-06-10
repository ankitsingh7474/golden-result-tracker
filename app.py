from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Golden Result Tracker</title>
    <meta http-equiv="refresh" content="10" />
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
    url = "https://mob.gnclott.com/QuickLink/ResultChart.aspx"
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        rows = table.find_all("tr")
        last = rows[-1]
        cols = last.find_all("td")
        if len(cols) < 5:
            return {"Error": "Unexpected format"}
        return {
            "Draw Time": cols[0].text.strip(),
            "Navratna": cols[1].text.strip(),
            "Rajarani": cols[2].text.strip(),
            "Royal": cols[3].text.strip(),
            "Golden": cols[4].text.strip(),
        }
    except:
        return {"Error": "Could not fetch result"}

@app.route("/")
def index():
    results = fetch_results()
    return render_template_string(HTML_TEMPLATE, results=results)

if __name__ == "__main__":
    app.run()
  
