# Hindustan-Times-TTC-News-Aggregator-Web-App

Sure! Here's your cleaned-up, professional-style `README` content **without stars, hashtags, or emojis**, using plain text formatting while keeping it structured and clear:

---

**Hindustan Times TTC – News Aggregator Web App**

Hindustan Times TTC is a modern, category-wise news aggregator built with Flask. It scrapes real-time headlines from the Hindustan Times website using BeautifulSoup and presents them in a clean, user-friendly interface with dark mode and bookmarking functionality.

---

Features

- Real-time news scraping by category (e.g., Economy, Sports, Films, etc.)
- Dark mode toggle with persistent local storage
- Bookmark your favorite headlines (stored in session)
- Refresh button to load the latest headlines
- Timestamp showing last fetched news
- Minimal, responsive UI using Google Fonts
- Pure JavaScript frontend without external frameworks

---

Supported News Categories

- Economy  
- Sports  
- Films  
- Trending  
- India  
- World  
- Technology  
- Lifestyle  
- Education  
- Health  
- Science  
- Environment  

---

Installation Guide

Step 1: Clone the Repository

```
git clone https://github.com/yourusername/hindustan-times-ttc.git
cd hindustan-times-ttc
```

Step 2: Install Required Dependencies

If a requirements.txt file exists:

```
pip install -r requirements.txt
```

Or install manually:

```
pip install flask requests beautifulsoup4
```

Step 3: Run the Application

```
python app.py
```

Step 4: Open in Browser

Visit: http://127.0.0.1:5000/

---
Now this will be become your output!
![Screenshot (18)](https://github.com/user-attachments/assets/c62b4d21-6381-4301-821f-e454f3b538a5)

How It Works

- News is scraped from Hindustan Times based on the selected category using requests and BeautifulSoup.
- The backend exposes a /api/news endpoint that returns news data in JSON format.
- Bookmarked headlines are stored in the Flask session and can be retrieved via /api/bookmarks.
- The frontend dynamically displays headlines and bookmarks using vanilla JavaScript.

---

Planned Enhancements

- AI-generated summaries for each headline
- Export option to save headlines as PDF
- User authentication and login system
- Daily email alerts with top headlines
- Support for scraping custom URLs with CSS selectors
- Persistent bookmark storage in a database (e.g., SQLite or MongoDB)

---

Authors

Developed by Bhuvaneswari Yennapusala and Sohith Bukka  
As part of a semester project in 2025

---

License

This project is licensed under the MIT License.

