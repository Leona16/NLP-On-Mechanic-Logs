from flask import Flask, request, render_template
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

app = Flask(__name__)

# Download required NLTK data (only runs first time)
nltk.download('punkt')
nltk.download('stopwords')

# Load dataset
df = pd.read_csv("dataset.csv")

# Stopwords
stop_words = set(stopwords.words('english'))

# Preprocessing function
def preprocess(text):
    words = word_tokenize(str(text).lower())
    filtered = [w for w in words if w.isalnum() and w not in stop_words]
    return set(filtered)

# NLP Matching Function
def simplify_log(user_input):
    user_words = preprocess(user_input)

    best_match = None
    max_score = 0

    for index, row in df.iterrows():
        problem = str(row['COMMON PROBLEM'])
        problem_words = preprocess(problem)

        score = len(user_words & problem_words)

        if score > max_score:
            max_score = score
            best_match = row

    if best_match is not None and max_score > 0:
        return f"Problem: {best_match['COMMON PROBLEM']} | Solution: {best_match['SOLUTION USED']}"

    return "No matching issue found. Please check manually."


# Main Route
@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    if request.method == 'POST':
        log = request.form['log']
        vehicle = request.form['vehicle']

        result = simplify_log(log)

        result = f"Vehicle Type: {vehicle.upper()} | {result}"

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)