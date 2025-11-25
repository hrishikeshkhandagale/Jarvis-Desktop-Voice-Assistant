from flask import Flask, request, render_template_string
import datetime
import wikipedia
import pyjokes

app = Flask(__name__)

HTML = """
<html>
<head>
<title>Jarvis Web Assistant</title>
<style>
body { background:#111; color:#0f0; font-family:consolas; padding:20px; }
input { width:80%; padding:10px; font-size:18px; }
button { padding:10px; font-size:18px; }
pre { background:#000; padding:20px; }
</style>
</head>
<body>
<h1>Jarvis Web Assistant</h1>
<form action="/" method="post">
    <input type="text" name="query" placeholder="Enter your command..." autofocus />
    <button type="submit">Send</button>
</form>

<h2>Response:</h2>
<pre>{{ output }}</pre>

</body>
</html>
"""

def jarvis_process(query):
    if not query:
        return "Please enter a valid command."

    query = query.lower()

    if "time" in query:
        return datetime.datetime.now().strftime("%I:%M:%S %p")

    if "date" in query:
        d = datetime.datetime.now()
        return f"{d.day}/{d.month}/{d.year}"

    if "wikipedia" in query:
        try:
            q = query.replace("wikipedia", "").strip()
            return wikipedia.summary(q, sentences=2)
        except:
            return "Wikipedia could not find anything."

    if "joke" in query:
        return pyjokes.get_joke()

    if "hello" in query or "hi" in query:
        return "Hello sir, Jarvis here!"

    return "Sorry, I didn't understand that."

@app.route("/", methods=["GET", "POST"])
def home():
    output = ""
    if request.method == "POST":
        user_query = request.form.get("query")
        output = jarvis_process(user_query)
    return render_template_string(HTML, output=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
