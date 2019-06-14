from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)
mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'cuenta@gmail.com'
app.config['MAIL_PASSWORD'] = 'contraseña'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/send', methods = ['POST'])
def data_email():
    content = request.json

    msg = Message('Tu informe ha cambiado de estado',
     sender = 'cuenta@gmail.com', recipients = [content['email']])

    msg.html = render_template('beefree.html', 
    name=content['name'],
     id_card=content['id_card'],
      state=content['state'])

    mail.send(msg)

    return "Sent"

if __name__ == '__main__':
    app.run(debug=True)