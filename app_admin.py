from flask import Flask, render_template, request, session, abort, redirect


app = Flask(__name__)


@app.route('/admin')
def index():
    return render_template('admin/index.html')


@app.route('/admin/singup', methods=['GET', 'POST'])
def singup():
    if request.method == 'GET':
        return render_template('/admin/singup.html')

    elif request.method == 'POST':
        username = request.form.get('username')
        print(username)
        password = request.form.get('password')
        email = request.form.get('email')
        ngaysinh = request.form.get('ngaysinh')
        gioitinh = request.form.get('gioitinh')

        query = "INSERT INTO user (username, password,ngaysinh,gioitinh, email ) VALUES('%s','%s','%s','%s,%s')" % (
            username, password, ngaysinh, gioitinh, email)
        print(query)

        return redirect('/admin/login')


@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('user_id'):
            return redirect('/')
        return render_template('/admin/login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = "SELECT * FROM user WHERE username='%s' AND password='%s' LIMIT 1" % (username, password)
        print(user)
        if user:
            session['user_id'] = user['id']
            return redirect('/')
        return redirect('/admin/login')


@app.route('/admin/search', methods=['GET'])
def search():
    name = request.args.get('name')
    data = []
    if name:
        user = "Select * from article A inner join category C on A.category_id = C.id  where name = %s" % name
        print(user)
    return render_template("/admin/search.html", data=data)



if __name__ == '__main__':
    app.run()
