from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    if current_question_id is not None:
        session["answers"].append(answer)
        return True, ""
    else:
        return False, "No question to answer."


def get_next_question(current_question_id):
    if current_question_id is not None:
        next_question_id = current_question_id + 1
        if next_question_id < len(PYTHON_QUESTION_LIST):
            return PYTHON_QUESTION_LIST[next_question_id], next_question_id
    return None, -1


def generate_final_response(session):
    score = len(session.get("answers", []))
    return f"Your final score is {score} out of {len(PYTHON_QUESTION_LIST)}."

