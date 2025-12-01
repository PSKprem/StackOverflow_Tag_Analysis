from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
from collections import defaultdict
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Read the CSV file on server start
DATA_FILE = 'final_data_stackoverflow_questions.csv'
Labels = [2022, 2023, 2024]

def load_and_process_data():
    df = pd.read_csv(DATA_FILE)
    data = {time : 0 for time in Labels}
    for year in df['year'].dropna():
        data[year] = data.get(year, 0) + 1
    return {"labels" : list(data.keys()), "values" : list(data.values())}

@app.route('/api/chart-data')
def get_question_stats():
    try:
        data = load_and_process_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def load_top_tags():
    filepath = os.path.join(os.path.dirname(__file__), 'final_data_stackoverflow_questions.csv')
    df = pd.read_csv(filepath)

    if 'tag' not in df.columns or 'timestamp' not in df.columns:
        return {}

    df['year'] = pd.to_datetime(df['timestamp'], errors='coerce').dt.year
    df = df[df['year'].isin([2022, 2023, 2024])]

    # Get overall top 10 tags from all years
    top_tags = df['tag'].str.lower().value_counts().nlargest(10).index.tolist()

    # Count total questions per year (approximated by unique Question No per year)
    total_per_year = df.groupby('year')['Question No'].nunique().to_dict()

    # Initialize frequency dict
    freq = {year: {tag: 0 for tag in top_tags} for year in [2022, 2023, 2024]}

    # Group tags by question to prevent double-counting in the same question
    grouped = df.groupby(['Question No', 'year'])['tag'].apply(
        lambda tags: set(str(tag).lower() for tag in tags if pd.notna(tag))
    )

    grouped_df = grouped.reset_index().rename(columns={'tag': 'tags'})

    for _, row in grouped_df.iterrows():
        year = row['year']
        tags = row['tags']
        if year in freq:
            for tag in top_tags:
                if tag in tags:
                    freq[year][tag] += 1

    # Normalize
    normalized_freq = {}
    for year in freq:
        total = total_per_year.get(year, 1)
        normalized_freq[year] = {
            tag: round(freq[year][tag] / total * 100, 4)
            for tag in top_tags
        }

    return normalized_freq

@app.route('/top-tags')
def top_tags():
    data = load_top_tags()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
