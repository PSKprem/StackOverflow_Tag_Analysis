# Stack Overflow Technologies Analysis

Analysis of how developer technology preferences changed over time, based on Stack Overflow question tags from **2022 to 2024**.

Question tags were scraped from Stack Overflow, cleaned into a CSV, and served through a small **Flask** API. A **Chart.js** frontend shows how often questions were asked each year and how the top 10 tags trended over the years.

## Features

- 📊 **Questions per year** - bar chart of how many scraped tag entries there are for each year.
- 📈 **Top 10 tag trends** - line chart of the 10 most-used tags across all years, showing the percentage of that year's questions that used each tag.
- 🧮 **Fair comparison** - a tag is counted only once per question, and counts are normalised by the number of unique questions in each year, so years with more data don't look inflated.

## Dataset

`final_data_stackoverflow_questions.csv` has **62,715 rows** (one row per question-tag pair) from **14,786 questions**.

| Column        | Description                                  |
|---------------|----------------------------------------------|
| `Question No` | Question identifier                          |
| `year`        | Year the question was asked                  |
| `timestamp`   | Question timestamp (e.g. `2024-02-03 18:03:53Z`) |
| `tag`         | One tag attached to the question             |

The most frequent tags in the dataset are python, javascript, java, c#, reactjs, r, html, android, flutter and c++.

## Tech Stack

| Layer    | Technology                               |
|----------|------------------------------------------|
| Scraping | Python, BeautifulSoup                    |
| Backend  | Python, Flask, Flask-CORS, Pandas        |
| Frontend | HTML, CSS, JavaScript, Chart.js          |
| Hosting  | PythonAnywhere (backend API)             |

## Project Structure

```
StackOverflow_Tag_Analysis/
├── app.py                                   # Flask API
├── final_data_stackoverflow_questions.csv   # Scraped dataset
└── frontend/
    └── index.html                           # Chart.js dashboard
```

## API Endpoints

| Method | Endpoint          | Description |
|--------|-------------------|-------------|
| GET    | `/api/chart-data` | Number of rows per year, returned as `{ "labels": [...], "values": [...] }` |
| GET    | `/top-tags`       | Top 10 tags with the percentage of each year's questions that used them: `{ "2022": { "python": 12.3, ... }, ... }` |

### How `/top-tags` is calculated

1. Convert `timestamp` to a year with `pd.to_datetime(..., errors="coerce")` and keep only 2022-2024.
2. Find the overall top 10 tags with `value_counts().nlargest(10)`.
3. Group tags by `(Question No, year)` into a set, so a tag is counted only once per question.
4. Divide each tag's count by the number of unique questions in that year and multiply by 100.

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/PSKprem/StackOverflow_Tag_Analysis.git
cd StackOverflow_Tag_Analysis

# 2. Install dependencies
pip install flask flask-cors pandas

# 3. Run the backend (http://127.0.0.1:5000)
python app.py
```

Then open `frontend/index.html` in a browser.

> **Note:** The frontend currently calls the hosted API at `https://premshankar.pythonanywhere.com`. To use your local backend, change the `fetch` URLs in `frontend/index.html` to `http://127.0.0.1:5000`.

## Future Improvements

- Use the official Stack Exchange API instead of scraping.
- Add 2025 data and monthly trend views.
- Let users choose which tags to compare.

## Author

**Prem Shankar Kushwaha** - [GitHub](https://github.com/PSKprem)
