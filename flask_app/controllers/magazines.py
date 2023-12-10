from flask_app import app
from flask_app.models.magazine import Magazine
from flask_app.models.user import User


from flask import request, render_template, session, redirect



# create new magazine
@app.route('/magazine/add-magazine')
def add_magazine():
    user = User.get_by_id({'id': session['user_id']})
    return render_template("add_magazine.html", logged_user = user)

@app.route('/magazine/create' , methods=['POST'])
def create():
    Magazine.create(request.form)
    return redirect('/dashboard')



#subscription
@app.route('/magazine/<int:id>/sub')
def subscribe(id):
    Magazine.add_user_sub({'users_id': session['user_id'] , 'magazines_id': id})
    return redirect('/dashboard')

#remove subscription
@app.route('/magazine/<int:id>/unsubscribe')
def unsubscribe(id):
    print({'users_id': session['user_id'] , 'magazines_id': id})
    Magazine.remove_user_sub({'users_id': session['user_id'] , 'magazines_id': id})
    return redirect('/dashboard')


@app.route('/magazine/<int:id>')
def show_magazine(id):
    magazine = Magazine.get_by_id2({'id': id})
    return render_template("magazine_details.html", magazine=magazine)


@app.route('/magazine/<int:id>/delete')
def delete(id):
    Magazine.delete({'id': id})
    return redirect('/user/account')
