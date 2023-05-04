from flask import render_template, url_for, redirect
from flask_login import current_user
from . import main



@main.route('/')
@main.route('/home')
def home():
    """
    Renders the home page of the application. If the user is authenticated, redirects to the transaction index page.

    Returns:
        A rendered HTML template.
    """
    if current_user.is_authenticated:
        return redirect(url_for(endpoint='transaction.index'))
    return render_template('main/home.html')