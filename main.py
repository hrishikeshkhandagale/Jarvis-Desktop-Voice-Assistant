from flask import Flask, request, render_template_string
import datetime
import wikipedia
import pyjokes
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# GOOGLE SEARCH SCRAPER
def google_search(query):
    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract first answer
        ans = soup.find("div", class_="BNeawe").text
        return ans

    except:
        return "No answer found."

# INTERNET SEARCH (fallback)
def internet_search(query):
    try:
        result = google_search(query)
        if result:
            return result
        else:
            return "Could not find answer."
    except:
        return "Search error."

# MAIN JARVIS LOGIC
def jarvis_process(query):
    if not query:
        return "Please enter something."

    q = query.lower()

    if "time" in q:
        return datetime.datetime.now().strftime("%I:%M:%S %p")

    if "date" in q:
        d = datetime.datetime.now()
        return f"{d.day}/{d.month}/{d.year}"

    if "wikipedia" in q:
        try:
            key = q.replace("wikipedia", "").strip()
            return wikipedia.summary(key, sentences=2)
        except:
            return "Wikipedia could not find anything."

    if "joke" in q:
        return pyjokes.get_joke()

    if any(word in q for word in ["hello", "hi"]):
        return "Hello Sir, Jarvis here!"

    # 🔥 SUPER SEARCH → Always returns meaningful answer
    return internet_search(query)

# HTML UI
HTML = """
<html>
<head>
<title>Jarvis Voice Assistant</title>
<style>
body { background:#0b0b0b; color:#00ffcc; font-family:Arial; text-align:center; padding:40px; }
#box { width:70%; margin:auto; background:rgba(255,255,255,0.05); padding:30px; border-radius:20px; box-shadow:0 0 20px #00ffcc; }
input { width:70%; padding:15px; font-size:18px; border-radius:10px; background:black; color:#00ffcc; border:2px solid #00ffcc; }
button { padding:12px 20px; font-size:18px; background:#00ffcc; border-radius:10px; border:none; cursor:pointer; }
button:hover { background:#00ffaa; }
pre { background:black; padding:20px; border-radius:10px; color:#00ffcc; text-align:left; }
</style>
</head>
<body>

<h1>⚡ JARVIS VOICE ASSISTANT ⚡</h1>

<div id="box">
<form action="/" method="post">
    <input type="text" name="query" placeholder="Ask Jarvis..." />
    <button type="submit">Send</button>
</form>

<h2>Response:</h2>
<pre>{{ output }}</pre>
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    output = ""
    if request.method == "POST":
        user_query = request.form.get("query")
        output = jarvis_process(user_query)
    return render_template_string(HTML, output=output)

app.run(host="0.0.0.0", port=5000)
