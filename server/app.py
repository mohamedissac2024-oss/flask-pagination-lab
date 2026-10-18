#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

import os
from config import create_app, db, api
from models import Book, BookSchema

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)


class Books(Resource):
    def get(self):
        # get page and per_page from the url, with default values
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        # get only the books for this page
        pagination = Book.query.paginate(page=page, per_page=per_page, error_out=False)

        # turn each book into a dictionary
        books = [BookSchema().dump(b) for b in pagination.items]

        # send back the books with the extra info
        return {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'total_pages': pagination.pages,
            'items': books
        }, 200


api.add_resource(Books, '/books', endpoint='books')


if __name__ == '__main__':
    app.run(port=5555, debug=True)