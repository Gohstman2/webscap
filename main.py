from flask import Flask
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/")
def test_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://example.com")
        title = page.title()
        browser.close()
        return f"Titre de la page : {title}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
