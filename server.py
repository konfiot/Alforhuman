from flask import Flask, session, redirect, request, render_template
import uuid
import random
from server_business.server_business import ServerBusiness
import os
import redis

redis_url = os.getenv('REDISTOGO_URL', '')

app = Flask(__name__)

if redis_url:
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis.from_url(redis_url)


app.secret_key = os.getenv('APP_SECRET', str(uuid.uuid1()))

DATASET_PATH = 'data/'
NUM_TRAIN_EXAMPLES = 5
NUM_TEST_EXAMPLES = 5
serverBusiness = ServerBusiness(db=True)  # change for local storage or use db


@app.route('/')
def root():
    if "id" not in session:
        session_id, questions = serverBusiness.start_session()
        session["id"] = session_id
        session["questions"] = questions

    return render_template("home.html", id=session["id"], questions=session["questions"])


@app.route("/user_form/", methods=["POST"])
def user_form():
    if "id" not in session:
        return redirect("/")

    serverBusiness.receive_form(
        session["id"], None)
    # Flip a coin to decide if we get Active Learning or Random
    al_type = random.randint(0, 1)
    serverBusiness.initialize_dataset(
        session["id"], 'color', al_type, DATASET_PATH)
    return redirect("/show_samples")


@app.route("/show_samples/")
def show_samples():
    if "id" not in session:
        return redirect("/")

    initial_dataset = serverBusiness.get_first_images(session["id"])

    return render_template("show_samples.html", dataset=zip(*initial_dataset))


@app.route("/show_question/")
def show_question():
    print(session)
    if "id" not in session:
        return redirect("/")
    is_testing = False
    if ("counter" not in session):
        session["counter"] = 0
        progress_bar = 0
        X_query, true_y, q = serverBusiness.start_active_learning(
            session["id"])  # get first query
    elif session["counter"] < NUM_TRAIN_EXAMPLES:  # get next query, still in train phase

        progress_bar = session['counter']/NUM_TRAIN_EXAMPLES
        X_query, true_y, q = serverBusiness.active_learning_iteration(
            session["id"])
    else:
        is_testing = True
        X_query, true_y, q = serverBusiness.test_iteration(session["id"])
        progress_bar = (session['counter'] -
                        NUM_TRAIN_EXAMPLES)/NUM_TEST_EXAMPLES
    session["true_y"] = int(true_y)
    session["q"] = q
    progress_bar = int(100*progress_bar)
    return render_template("show_question.html", X=X_query, is_testing=is_testing, progress_bar=progress_bar)


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

    if session["counter"] < NUM_TRAIN_EXAMPLES:  # train phase, show feedback
        serverBusiness.store_active_learning_pred(
            session["id"], answer, session["q"])  # store previous answer
        session["counter"] += 1
        good = int(session['true_y'] == answer)
        return redirect(f"/feedback/{good}")
    # test phase, dont show feedback directly ask other question. TODO show question with flag indicating that it is test time
    elif session["counter"] == NUM_TRAIN_EXAMPLES :
        session["counter"] += 1
        return render_template("announcement.html", message="Testing phase, you won't receive feedback. ")
    elif session["counter"] < NUM_TRAIN_EXAMPLES + NUM_TEST_EXAMPLES:
        session["counter"] += 1
        # store previous answer
        serverBusiness.store_pred(session["id"], answer, session["q"])
        return redirect("/show_question")
    else:
        session["counter"] += 1
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
    serverBusiness.signal_end_experiment(session["id"])
    return render_template("announcement.html", message='Thank you!')
