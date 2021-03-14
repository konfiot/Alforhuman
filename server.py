from server_business import start_session, receive_form
from flask import Flask, session, redirect, request, render_template
import uuid
app = Flask(__name__)
app.secret_key = str(uuid.uuid1())# TODO: get from file

@app.route('/')
def root():
	if "id" not in session:
		session_id, questions = start_session()
		session["id"] = session_id
		session["questions"] = questions

	return render_template("home.html", id=session["id"], questions=session["questions"])

@app.route("/questions/", methods=["GET", "POST"])
def user_form():
	if "id" not in session or request.method != "POST":
		return redirect("/")
	
	for key in session["questions"].keys():
		if key not in request.form:
			return redirect("/")
		else:
			session[key] = request.form[key] # TODO : Sanitize
	
	return redirect("/show_sample")


@app.route("/show_sample/")
def samples():
	if "id" not in session:
		return redirect("/")

	dataset = receive_form(session["id"], {k:session[k] for k in session["questions"].keys()})
	return render_template("examples.html", dataset=zip(*dataset))
