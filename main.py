from flask import Flask, render_template, request, make_response, current_app
from flask_mail import Mail, Message
from datetime import timedelta  
from functools import update_wrapper


app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'evernext10@gmail.com'
app.config['MAIL_PASSWORD'] = 'XXXXX'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):  
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route('/send', methods=['POST'])
@crossdomain(origin='*')
def data_email():
    content = request.json
    email = content['email']
    name = content['name']
    id_card = content['id_card']
    state = content['state']

    msg = Message("Hello",
                  sender=("Me", "expeditepay@gmail.com"))
    msg.recipients = [email]
    msg.html = render_template('beefree.html',
                               name=name,
                               id_card=id_card,
                               state=state)

    mail.send(msg)
    response = {}
    reponse['code'] = 200
    response['result'] = 'Sucess'
    return response


if __name__ == '__main__':
    app.run(debug=True)
