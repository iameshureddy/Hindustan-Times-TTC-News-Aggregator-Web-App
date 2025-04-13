from flask import Flask, jsonify, render_template_string, request, session
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'

CATEGORY_URLS = {
    "economy": "https://www.hindustantimes.com/business",
    "sports": "https://www.hindustantimes.com/sports",
    "films": "https://www.hindustantimes.com/entertainment/bollywood",
    "trending": "https://www.hindustantimes.com/trending",
    "india": "https://www.hindustantimes.com/india-news",
    "world": "https://www.hindustantimes.com/world-news",
    "technology": "https://www.hindustantimes.com/technology",
    "lifestyle": "https://www.hindustantimes.com/lifestyle",
    "education": "https://www.hindustantimes.com/education",
    "health": "https://www.hindustantimes.com/lifestyle/health",
    "science": "https://www.hindustantimes.com/science",
    "environment": "https://www.hindustantimes.com/environment"
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hindustan Times TTC</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #e0f7fa;
            --text: #111;
            --container-bg: rgba(255, 255, 255, 0.8);
        }

        body.dark-mode {
            --bg: #1e1e2f;
            --text: #f9f9f9;
            --container-bg: rgba(30, 30, 47, 0.9);
        }

        body {
            font-family: 'Outfit', sans-serif;
            background: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 0;
            transition: 0.3s ease-in-out;
        }

        header {
            background: #0a043c;
            color: white;
            padding: 30px 10px;
            text-align: center;
            position: relative;
        }

        .toggle-darkmode {
            position: absolute;
            top: 20px;
            right: 20px;
            padding: 10px;
            background: #ffffff22;
            border: none;
            border-radius: 50%;
            font-size: 18px;
            cursor: pointer;
        }

        .container {
            max-width: 900px;
            margin: 40px auto;
            padding: 40px;
            background: var(--container-bg);
            border-radius: 20px;
        }

        h2 {
            text-align: center;
        }

        select, button {
            padding: 12px;
            border-radius: 10px;
            margin: 10px;
            border: none;
            font-size: 16px;
        }

        button:hover {
            background: #ddd;
            cursor: pointer;
        }

        ul {
            list-style: none;
            padding: 0;
        }

        li {
            background: #fff;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        body.dark-mode li {
            background: #2e2e42;
        }

        li a {
            text-decoration: none;
            font-weight: 600;
            color: #003566;
        }

        body.dark-mode li a {
            color: #ffffff;
        }

        li button {
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
        }

        #timestamp {
            margin: 10px 0;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <header>
        <h1>📰 Hindustan Times TTC</h1>
        <button class="toggle-darkmode" onclick="toggleDarkMode()">🌙</button>
    </header>
    <div class="container">
        <h2>Latest News by Category</h2>
        <div style="text-align: center;">
            <select id="category">
                {% for key in categories %}
                    <option value="{{ key }}">{{ key.title() }}</option>
                {% endfor %}
            </select>
            <button onclick="getNews()">🔁 Refresh</button>
            <button onclick="viewBookmarks()">🔖 Bookmarks</button>
        </div>
        <div id="timestamp" style="text-align: center;"></div>
        <ul id="newsList"></ul>
    </div>
    <script>
        function toggleDarkMode() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        }

        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
        }

        function getNews() {
            const cat = document.getElementById('category').value;
            fetch(`/api/news?category=${cat}`)
            .then(res => res.json())
            .then(data => {
                const list = document.getElementById('newsList');
                list.innerHTML = '';
                if (data.news) {
                    data.news.forEach(item => {
                        const li = document.createElement('li');
                        li.innerHTML = `<a href="${item.url}" target="_blank">${item.title}</a>
                            <button onclick="bookmark('${item.title}', '${item.url}')">🔖</button>`;
                        list.appendChild(li);
                    });
                    document.getElementById('timestamp').innerText = "🕒 " + data.news[0].fetched_at;
                } else {
                    list.innerHTML = '<li>No news found.</li>';
                }
            });
        }

        function bookmark(title, url) {
            fetch('/api/bookmark', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, url })
            }).then(() => alert("Bookmarked!"));
        }

        function viewBookmarks() {
            fetch('/api/bookmarks')
            .then(res => res.json())
            .then(data => {
                const list = document.getElementById('newsList');
                list.innerHTML = '';
                data.bookmarks.forEach(item => {
                    const li = document.createElement('li');
                    li.innerHTML = `<a href="${item.url}" target="_blank">${item.title}</a>`;
                    list.appendChild(li);
                });
                document.getElementById('timestamp').innerText = "🔖 Your Bookmarks";
            });
        }

        window.onload = getNews;
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, categories=CATEGORY_URLS)

@app.route('/api/news')
def get_news():
    category = request.args.get('category', '').lower()
    url = CATEGORY_URLS.get(category)
    if not url:
        return jsonify({'error': 'Invalid category'}), 400

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select('h3 a, a:has(h3)')

        news = []
        for a in articles:
            title = a.get_text(strip=True)
            link = a.get('href', '')
            if title and link:
                if not link.startswith("http"):
                    link = "https://www.hindustantimes.com" + link
                news.append({
                    "title": title,
                    "url": link,
                    "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
            if len(news) >= 15:
                break

        return jsonify({"news": news})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookmark', methods=['POST'])
def bookmark():
    data = request.json
    if 'bookmarks' not in session:
        session['bookmarks'] = []
    session['bookmarks'].append(data)
    session.modified = True
    return '', 204

@app.route('/api/bookmarks')
def get_bookmarks():
    return jsonify({'bookmarks': session.get('bookmarks', [])})

if __name__ == '__main__':
    app.run(debug=True)