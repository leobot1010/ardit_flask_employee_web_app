from datetime import datetime
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["SECRET_KEY"] = "myapp303"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "leobot1010@gmail.com"
app.config["MAIL_PASSWORD"] = "vuihokpyyfphutnc"

db = SQLAlchemy(app)

mail = Mail(app)


@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]

        date_str = request.form["date"]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        occupation = request.form["occupation"]

        form = Form(first_name=first_name, last_name=last_name,
                    email=email, date=date_obj, occupation=occupation)

        db.session.add(form)
        db.session.commit()

        message_body = f"Thanks for your submission, {first_name}. \n" \
                       f"Here are your entered details:\n\n" \
                       f"Name: {first_name} {last_name}\n" \
                       f"Email: {email}\n" \
                       f"Start Date: {date_str}\n" \
                       f"Occupation Status: {occupation}"

        message = Message(subject='Your Form Submission',
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)
        mail.send(message)

        flash(f"Thanks {first_name}, your form was submitted successfully!\n"
              f"You will receive an email containing your inputted details.", "success")

    return render_template("home.html")



class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)




