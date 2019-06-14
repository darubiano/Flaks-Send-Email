from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'evernext10@gmail.com'
app.config['MAIL_PASSWORD'] = 'XXXXX'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/send', methods=['POST'])
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
    return 'Se envio'


if __name__ == '__main__':
    app.run(debug=True)
