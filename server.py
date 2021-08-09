from server_business import *
from flask import Flask, session, redirect, request, render_template
import uuid
import random
app = Flask(__name__)
app.secret_key = str(uuid.uuid1())# TODO: get from file

DATASET_PATH = 'data/'
NUM_TRAIN_EXAMPLES =  5
NUM_TEST_EXAMPLES = 5
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

	receive_form(session["id"], {k:session[k] for k in session["questions"].keys()})
	al_type = random.randint(0, 1) # Flip a coin to decide if we get Active Learning or Random
	initialize_dataset(session["id"], 'color', al_type, DATASET_PATH)
	return redirect("/show_samples")


@app.route("/show_samples/")
def show_samples():
	if "id" not in session:
		return redirect("/")

	initial_dataset = get_first_images(session["id"])
	print('test')
	print(initial_dataset)
	return render_template("show_samples.html", dataset=zip(*initial_dataset))


@app.route("/show_question/")
def show_question():
	if "id" not in session:
		return redirect("/")

	if ("counter" not in session):
		session["counter"] = 0
		X_query, true_y, q = start_active_learning(session["id"]) # get first query
	elif session["counter"] < NUM_TRAIN_EXAMPLES:# get next query, still in train phase
		X_query, true_y, q = active_learning_iteration(session["id"]) 
	else:
		X_query, true_y, q = test_iteration(session["id"]) 
		
	session["true_y"] = int(true_y)
	session["q"] = q
	return render_template("show_question.html", X=X_query)

@app.route("/answer_question/<int:answer>")
def get_answer(answer):
	if "id" not in session:
		return redirect("/")
	
	if answer not in [0, 1]:
		return redirect("/")

	if ("counter" not in session
	or "q" not in session
	or "true_y" not in session):
		return redirect("/show_question")
	
	store_active_learning_pred(session["id"], answer, session["q"]) # store previous answer
	session["counter"] += 1
	if session["counter"] < NUM_TRAIN_EXAMPLES: # train phase, show feedback
		good = int(session['true_y'] == answer)
		return redirect(f"/feedback/{good}")
	elif session["counter"] < NUM_TRAIN_EXAMPLES + NUM_TEST_EXAMPLES: # test phase, dont show feedback directly ask other question. TODO show question with flag indicating that it is test time
		return redirect("/show_question")
	else:
		return redirect("/finished")
	

@app.route("/feedback/<int:good>")
def feedback(good):
	if "id" not in session:
		print("ID not in session")
		return redirect("/")
	
	if good not in [0, 1]:
		return redirect("/")

	return render_template("show_result.html", result=good)

@app.route("/finished")
def finished():
	if "id" not in session:
		return redirect("/")
	signal_end_experiment(session["id"])
	return "kthxbye"
