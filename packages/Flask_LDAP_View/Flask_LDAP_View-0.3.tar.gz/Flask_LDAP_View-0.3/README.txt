# Flask LDAP View
A library to restrict your flask pages by LDAP groups

A more full example that includes Flask-Login can be found [here](https://github.com/sonance207/Flask_LDAP_View/blob/master/examples/example_Flask_LDAP_View.py).


## Installation

Install the extension with the following command:

```sh
$ pip install Flask_LDAP_View
```


## Usage

We start the  Flask LDAP View by instantiating it and telling it about our Flask app:

```python
from flask import Flask, g, redirect, session
from Flask_LDAP_View import LDAP_VIEW


app = Flask(__name__)

ldap = LDAP_VIEW(app)
```

Next we have to import our LDAP configuration 

```python
#Service account to search ldap tree
app.config['LDAP_HOST'] = 'ldap://127.0.0.1:389/'
app.config['LDAP_BASE_DN'] = 'OU=Admins,OU=Users,DC=exampleDC,DC=local'
app.config['LDAP_USERNAME'] = 'CN=User,OU=Admins,OU=Users,DC=exampleDC,DC=local'
app.config['LDAP_PASSWORD'] = 'password'

#Splash page to appear when user access a unauthorized resource
app.config['LDAP_UNAUTHORIZED_REDIRECT'] = '/unauthorized'
```

After that we will add our before request,views, and login
```python

@app.before_request
def before_request():
    try:
        g.user_memberof = session['user_memberof']
    except:
        session['user_memberof'] = None
        g.user_memberof = session['user_memberof']
        

@app.route('/')
def index():
    return 'Successfully logged in!'
    
@app.route('/unauthorized')
def unauthorized():
    return 'You are unauthorized to access this page'
    

def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['user']
        passwd = request.form['passwd']
        g.user_memberof = ldap.bind_user(username, passwd)
        if type(g.user_memberof) == ValueError:
            flash(g.user_memberof.message)
            return redirect('/login')
        session['user_memberof'] = g.user_memberof
        flash('You have successfully logged in')
        return redirect('/')
    else:
        redirect('/login')
    return """<form action="" method="post">
                user: <input name="user"><br>
                password:<input type="password" name="passwd"><br>
                <input type="submit" value="Submit"></form>"""

```

Now we're ready to define our views. In this example we are restricting access to the 
QA group
 
```python
@app.route('/group')
@ldap.group_required(['QA'])
def group():
    return 'You have been granted access to the Group restricted page '
```

You keep even use Flask-Login alongside with it.

```python
@app.route('/group')
@login_required
@ldap.group_required(['QA'])
def group():
    return 'You have been granted access to the Group restricted page '
```

A more full example that includes Flask-Login can be found [here](https://github.com/sonance207/Flask_LDAP_View/blob/master/examples/example_Flask_LDAP_View.py).
