from flask import session, request, redirect, url_for
import hashlib

def login_route(app):
    @app.route('/login', methods = ['GET','POST'])
    def login():
        failed = ""
        session['email'] = ""
        return session