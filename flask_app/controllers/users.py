
from flask_app import app
from flask_app.models.user import User
from flask_app.models.magazine import Magazine
from flask import render_template , request, redirect, session

@app.route('/')
def log_reg():
    if 'user_id' in session:
        return redirect('/dashboard')

    return render_template('main_page.html')


@app.route('/register', methods = ['POST'])
def register():
    data = request.form
    print(data)
    if User.validate_register(data):
        User.create(data)
    return redirect('/')

@app.route('/login' , methods=['POST'])
def login():
    data = request.form
    if User.validate_login(data):
        user = User.get_by_email(data)
        session["user_id"] = user.id
        return redirect("/dashboard")
    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        return redirect('/')
    magazines = Magazine.get_all()
    user = User.get_by_id({'id': session['user_id']})

    return render_template("dashboard.html", logged_user = user, magazines = magazines)



@app.route('/update', methods=['POST'])
def update():
    data = dict(request.form)
    user_id = session.get('user_id')

    if user_id:
        # Update user data in the database using the User model's update method
        User.update(data, user_id)

    return redirect('/user/account')



@app.route('/user/account')
def account():
    user_id = session.get('user_id')
    user_id = session.get('user_id')
    user = User.get_by_id({'id': user_id})
    user_magazines = Magazine.get_user_magazines(user_id)

    return render_template("account.html", user=user, user_magazines=user_magazines)

@app.route('/magazine/<int:id>/subscribe')
def subscribe_magazine(id):
    user_id = session.get('user_id')
    if user_id:
        Magazine.add_user_sub({'users_id': user_id, 'magazines_id': id})
    return redirect('/dashboard')


@app.route('/magazine/<int:id>/unsubscribe')
def unsubscribe_magazine(id):
    user_id = session.get('user_id')
    if user_id:
        Magazine.remove_user_sub({'users_id': user_id, 'magazines_id': id})
    return redirect('/dashboard')
