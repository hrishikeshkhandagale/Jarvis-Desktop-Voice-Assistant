from flask import Flask, request, render_template_string
import datetime
import wikipedia
import pyjokes
import requests

app = Flask(__name__)

HTML = """
<html>
<head>
<title>JARVIS Web Assistant</title>
<style>
body {
    background: linear-gradient(135deg, #0a0a0a, #1c1c1c);
    color: #0f0;
    font-family: Consolas;
    padding: 40px;
    text-align: center;
}

.container {
    width: 60%;
    margin: auto;
    padding: 30px;
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    box-shadow: 0 0 20px #00ff88;
    backdrop-filter: blur(10px);
}

input {
    width: 80%;
    padding: 12px;
    font-size: 18px;
    border-radius: 10px;
    border: 2px solid #00ff88;
    background: #000;
    color: #0f0;
}

button {
    padding: 12px 20px;
    font-size: 18px;
    background: #00ff88;
    color: #000;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    transition: 0.3s;
}

button:hover {
    background: #0f0;
}

pre {
    margin-top: 20px;
    background: #000;
    padding: 20px;
    border-radius: 10px;
    text-align: left;
    color: #0f0;
    box-shadow: 0 0 10px #00ff88;
}
</style>
</head>
<body>

<h1 style="color:#00ff88; text-shadow:0 0 10px #00ff88;">⚡ JARVIS WEB ASSISTANT ⚡</h1>

<div class="container">
<form action="/" method="post">
    <input type="text" name="query" placeholder="Ask Jarvis anything..." autofocus />
    <br><br>
    <button type="submit">Ask</button>
</form>

<h2 style="color:#00ff88;">Response:</h2>
<pre>{{ output }}</pre>
</div>

</body>
</html>
"""

# 🔥 DuckDuckGo search API
def internet_search(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&pretty=1"
        data = requests.get(url).json()
        if data.get("AbstractText"):
            return data["AbstractText"]
        else:
            return "No direct answer found — but here is a related link:\n" + data.get("AbstractURL", "Not available")
    except:
        return "Internet search failed."

def jarvis_process(query):
    if not query:
        return "Please enter a valid command."

    q = query.lower()

    if "time" in q:
        return datetime.datetime.now().strftime("%I:%M:%S %p")

    if "date" in q:
        d = datetime.datetime.now()
        return f"{d.day}/{d.month}/{d.year}"

    if "wikipedia" in q:
        try:
            ask = q.replace("wikipedia", "").strip()
            return wikipedia.summary(ask, sentences=2)
        except:
            return "Wikipedia error or no results."

    if "joke" in q:
        return pyjokes.get_joke()

    if any(word in q for word in ["hello", "hi", "hey"]):
        return "Hello Sir, Jarvis here! How can I assist you?"

    # 🔥 ANY query → Internet Search  
    return internet_search(query)

@app.route("/", methods=["GET", "POST"])
def home():
    output = ""
    if request.method == "POST":
        user_query = request.form.get("query")
        output = jarvis_process(user_query)
    return render_template_string(HTML, output=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
