from flask import Blueprint, request, jsonify
from src.database import Bookmark, db
import validators
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
from flask_jwt_extended import get_jwt_identity, jwt_required


bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")

@bookmarks.route("/", methods=["GET", "POST"])
@jwt_required()
def handle_bookmarks():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        body = request.get_json().get("body", "")
        url = request.get_json().get("url", "")
        print(url)

        if not validators.url(url):
            return jsonify({
                "error": "Enter a valid url!"
            }), HTTP_400_BAD_REQUEST
        
        if Bookmark.query.filter_by(url=url).first():
            return jsonify({
                "error": "URL already exist!"
            }), HTTP_409_CONFLICT

        bookmark = Bookmark(url=url, body=body, user_id=current_user)
        db.session.add(bookmark)
        db.session.commit()

        return jsonify({
            "id": bookmark.id,
            "url": bookmark.url, 
            "short_url": bookmark.short_url,
            "visits": bookmark.visits,
            "body": bookmark.body,
            "created_at": bookmark.created_at,
            "updated_at": bookmark.updated_at
        }), HTTP_201_CREATED
    
    else:
        bookmarks = Bookmark.query.filter_by(user_id=current_user)
        data = []
        for bookmark in bookmarks:
            data.append({
                "id": bookmark.id,
                "url": bookmark.url, 
                "short_url": bookmark.short_url,
                "visits": bookmark.visits,
                "body": bookmark.body,
                "created_at": bookmark.created_at,
                "updated_at": bookmark.updated_at
            })

        return jsonify({"data": data}), HTTP_200_OK
