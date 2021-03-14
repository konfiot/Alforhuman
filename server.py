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

@app.route("/user_form/", methods=["POST"])
def user_form():
	if "id" not in session:
		return redirect("/")

	for key in session["questions"].keys():
		if key not in request.form:
			return redirect("/")
		else:
			session[key] = request.form[key] # TODO : Sanitize

	return redirect("/show_samples")


@app.route("/show_samples/")
def show_samples():
	if "id" not in session:
		return redirect("/")

	dataset = receive_form(session["id"], {k:session[k] for k in session["questions"].keys()})
	return render_template("show_samples.html", dataset=zip(*dataset))


@app.route("/show_question/")
def show_question():
	if "id" not in session:
		return redirect("/")

	if "counter" not in session:
		session["counter"] = 0

	X_query, true_y, q = start_active_learning(session_id)

	session["true_y"] = true_y
	session["q"] = q
	return render_template("show_question.html", X=X_query)

@app.route("/get_answer/", methods=["POST"])
def get_answer():
	if "id" not in session:
		return redirect("/")

	if ("counter" not in session
	or "q" not in session
	or "true_y" not in session
	or "answer" not in request.form):
		return redirect("/show_question")

	dataset = get_dataset_of_session(session_id)
	dataset.add_human_prediction(request.form["answer"], session["q"])

	session["counter"] += 1

	if session["counter"] > 5:
		return redirect("/finished")

	return redirect("/show_question")



