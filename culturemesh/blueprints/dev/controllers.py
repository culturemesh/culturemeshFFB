from flask import Blueprint, render_template

dev = Blueprint('dev', __name__, template_folder='templates')

@dev.route("/note")
def get_note():
    return render_template("note.html")
