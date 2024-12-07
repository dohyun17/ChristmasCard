from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Letter

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/write', methods=['GET', 'POST'])
def write_letter():
    if request.method == 'POST':
        sender = request.form['sender']
        content = request.form['content']
        letter = Letter(sender=sender, content=content)
        db.session.add(letter)
        db.session.commit()
        return redirect(url_for('letter_list'))
    return render_template('write_letter.html')

@app.route('/letters')
def letter_list():
    letters = Letter.query.order_by(Letter.created_at.desc()).all()
    return render_template('letter_list.html', letters=letters)

@app.route('/letter/<int:id>')
def letter_detail(id):
    letter = Letter.query.get_or_404(id)
    return render_template('letter_detail.html', letter=letter)