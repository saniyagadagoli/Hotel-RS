from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, instance_relative_config=True)

# Secret key for session management and flash messages
app.config['SECRET_KEY'] = 'a1f9c8e7b6d5f4e3d2c1b0a9f8e7d6c5'

# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# Database configuration - stored inside instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'example.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ---------------- MODEL ----------------
class HotelGuest(db.Model):
    __tablename__ = 'hotel_registration'

    id = db.Column(db.Integer, primary_key=True)
    guest_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    room_number = db.Column(db.String(10), nullable=False)
    check_in = db.Column(db.String(20), nullable=False)
    check_out = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Guest {self.guest_name}>'


# Create tables if they do not already exist
with app.app_context():
    db.create_all()


# ---------------- ROUTES (CRUD) ----------------

# READ - Home page, list all guests
@app.route('/')
def index():
    guests = HotelGuest.query.all()
    return render_template('index.html', guests=guests)


# CREATE - Add new guest
@app.route('/add', methods=['POST'])
def add_guest():
    guest_name = request.form.get('guest_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    room_number = request.form.get('room_number')
    check_in = request.form.get('check_in')
    check_out = request.form.get('check_out')

    if not guest_name or not email or not phone or not room_number:
        flash('Please fill in all required fields!', 'error')
        return redirect(url_for('index'))

    new_guest = HotelGuest(
        guest_name=guest_name,
        email=email,
        phone=phone,
        room_number=room_number,
        check_in=check_in,
        check_out=check_out
    )
    db.session.add(new_guest)
    db.session.commit()
    flash('Guest registered successfully!', 'success')
    return redirect(url_for('index'))


# UPDATE - Edit existing guest
@app.route('/update/<int:id>', methods=['POST'])
def update_guest(id):
    guest = HotelGuest.query.get_or_404(id)

    guest.guest_name = request.form.get('guest_name')
    guest.email = request.form.get('email')
    guest.phone = request.form.get('phone')
    guest.room_number = request.form.get('room_number')
    guest.check_in = request.form.get('check_in')
    guest.check_out = request.form.get('check_out')

    db.session.commit()
    flash('Guest record updated successfully!', 'success')
    return redirect(url_for('index'))


# DELETE - Remove guest
@app.route('/delete/<int:id>')
def delete_guest(id):
    guest = HotelGuest.query.get_or_404(id)
    db.session.delete(guest)
    db.session.commit()
    flash('Guest record deleted successfully!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)