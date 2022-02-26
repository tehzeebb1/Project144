from flask import Flask, jsonify, request

from storage import all_articles, liked_articles, not_liked_articles, did_not_watch
from demographic_filtering import output
from content_filtering import get_recommendations

app = Flask(__name__)

@app.route("/get-articles")
def get_articlese():
    articles_data = {
        "title": all_articles[0][19],
        "poster_link": all_articles[0][27],
        "release_date": all_articles[0][13] or "N/A",
        "duration": all_articles[0][15],
        "rating": all_articles[0][20],
        "overview": all_articles[0][9]
    }
    return jsonify({
        "data": articles_data,
        "status": "success"
    })

@app.route("/liked-articles", methods=["POST"])
def liked_articles():
    articles = all_articles[0]
    liked_articles.append(articles)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/unliked-articles", methods=["POST"])
def unliked_articles():
    articles = all_articles[0]
    not_liked_articles.append(articles)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/did-not-watch", methods=["POST"])
def did_not_watch_view():
    articles = all_articles[0]
    did_not_watch.append(articles)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/popular-articles")
def popular_articles():
    articles_data = []
    for articles in output:
        _d = {
            "title": articles[0],
            "poster_link": articles[1],
            "release_date": articles[2] or "N/A",
            "duration": articles[3],
            "rating": articles[4],
            "overview": articles[5]
        }
        articles_data.append(_d)
    return jsonify({
        "data": articles_data,
        "status": "success"
    }), 200

@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_articles in liked_articles:
        output = get_recommendations(liked_articles[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    articles_data = []
    for recommended in all_recommended:
        _d = {
            "title": recommended[0],
            "poster_link": recommended[1],
            "release_date": recommended[2] or "N/A",
            "duration": recommended[3],
            "rating": recommended[4],
            "overview": recommended[5]
        }
        articles_data.append(_d)
    return jsonify({
        "data": articles_data,
        "status": "success"
    }), 200

if __name__ == "__main__":
  app.run()