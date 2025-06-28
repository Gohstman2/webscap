from flask import Flask, jsonify, send_file, request
from playwright.sync_api import sync_playwright
import os

app = Flask(__name__)

@app.route("/")
def index():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://example.com")
            title = page.title()
            browser.close()
        return jsonify({"success": True, "title": title})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
@app.route("/capture")
def capture():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Paramètre 'url' manquant"}), 400

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=15000)  # 15s timeout
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                screenshot_path = tmp_file.name
            page.screenshot(path=screenshot_path, full_page=True)
            browser.close()

        return send_file(
            screenshot_path,
            mimetype="image/png",
            as_attachment=False,
            download_name="screenshot.png"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render fournit automatiquement une variable d'environnement PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
