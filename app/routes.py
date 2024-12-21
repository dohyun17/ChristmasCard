from flask import render_template, request, redirect, url_for, flash
from app import db
from app.models import Letter

from flask import Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/write', methods=['GET', 'POST'])
def write_letter():
    if request.method == 'POST':
        sender = request.form['sender']
        content = request.form['content']
        letter = Letter(sender=sender, content=content)
        db.session.add(letter)
        db.session.commit()
        flash('편지가 성공적으로 작성되었습니다.')
        return redirect(url_for('main.letter_list'))
    return render_template('write_letter.html')

@main.route('/letters')
def letter_list():
    letters = Letter.query.order_by(Letter.created_at.desc()).all()
    return render_template('letter_list.html', letters=letters)

@main.route('/letter/<int:id>')
def letter_detail(id):
    letter = Letter.query.get_or_404(id)
    return render_template('letter_detail.html', letter=letter)

@main.route('/letter/<int:id>/edit', methods=['GET', 'POST'])
def edit_letter(id):
    letter = Letter.query.get_or_404(id)
    if request.method == 'POST':
        letter.sender = request.form['sender']
        letter.content = request.form['content']
        db.session.commit()
        flash('편지가 성공적으로 수정되었습니다.')
        return redirect(url_for('main.letter_detail', id=letter.id))
    return render_template('edit_letter.html', letter=letter)

@main.route('/letter/<int:id>/delete', methods=['POST'])
def delete_letter(id):
    letter = Letter.query.get_or_404(id)
    db.session.delete(letter)
    db.session.commit()
    flash('편지가 성공적으로 삭제되었습니다.')
    return redirect(url_for('main.letter_list'))

@main.route('/letter/<int:id>/share')
def share_letter(id):
    letter = Letter.query.get_or_404(id)
    share_url = url_for('main.letter_detail', id=letter.id, _external=True)
    return render_template('share_letter.html', letter=letter, share_url=share_url)
