from flask import Flask, request, render_template_string
import datetime
import wikipedia
import pyjokes
import requests

app = Flask(__name__)

# Internet Search
def internet_search(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&pretty=1"
        data = requests.get(url).json()
        if data.get("AbstractText"):
            return data["AbstractText"]
        else:
            return "No direct answer found — Here is a related link:\n" + data.get("AbstractURL", "Not available")
    except:
        return "Internet search failed."

# Jarvis Logic
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
            return "Wikipedia error or no results."

    if "joke" in q:
        return pyjokes.get_joke()

    if any(word in q for word in ["hello", "hi", "hey"]):
        return "Hello Sir, Jarvis here!"

    # Fallback — Internet Search
    return internet_search(query)

# HTML UI
HTML = """
<html>
<head>
<title>Jarvis Voice Assistant</title>
<style>
body {
    background: #0d0d0d;
    color: #00ffcc;
    font-family: Arial;
    text-align: center;
    padding: 40px;
}

#box {
    width: 70%;
    margin: auto;
    background: rgba(255,255,255,0.05);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 0 20px #00ffcc;
}

input {
    width: 70%;
    padding: 15px;
    font-size: 18px;
    border-radius: 10px;
    background: black;
    color: #00ffcc;
    border: 2px solid #00ffcc;
}

button {
    padding: 12px 20px;
    font-size: 18px;
    background: #00ffcc;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    margin-left: 10px;
}

button:hover {
    background: #00ffaa;
}

#micBtn {
    width: 60px;
    height: 60px;
    background: #00ffaa;
    border-radius: 50%;
    border: none;
    cursor: pointer;
    box-shadow: 0 0 20px #00ffaa;
    animation: glow 1.5s infinite alternate;
}

@keyframes glow {
    from { box-shadow: 0 0 10px #00ffaa; }
    to { box-shadow: 0 0 25px #00ffaa; }
}

pre {
    text-align: left;
    background: black;
    padding: 20px;
    border-radius: 10px;
    color: #00ffcc;
}
</style>

<script>
// Speech-to-Text
function startListening() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";

    recognition.onresult = function(event) {
        const text = event.results[0][0].transcript;
        document.getElementById("query").value = text;
    };

    recognition.start();
}

// Text-to-Speech
function speak(text) {
    const speech = new SpeechSynthesisUtterance(text);
    speech.pitch = 1;
    speech.rate = 1;
    speech.voice = window.speechSynthesis.getVoices()[1];
    speechSynthesis.speak(speech);
}
</script>

</head>
<body>

<h1>⚡ JARVIS VOICE ASSISTANT ⚡</h1>

<div id="box">

<form action="/" method="post">
    <input type="text" id="query" name="query" placeholder="Ask Jarvis..." />
    <button type="submit">Send</button>
    <button id="micBtn" type="button" onclick="startListening()">🎤</button>
</form>

<h2>Response:</h2>
<pre id="op">{{ output }}</pre>

<script>
    var rsp = "{{ output }}";
    if (rsp.length > 1) {
        speak(rsp);
    }
</script>

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
