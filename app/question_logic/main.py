from question_model import Question
from data import get_data
from quiz_brain import QuizBrain
from ui import Quizinterface

question_bank = []
for question in get_data():
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)

quiz = QuizBrain(question_bank)
quiz_interface = Quizinterface(quiz)
# while quiz.still_has_questions():
#     quiz.next_question()

# print("You've completed the quiz")
# print(f"Your final score was: {quiz.score}/{quiz.question_number}")



# age: int
# hwight: bool
#
#
# def police(age: int) -> bool:
#     if age >= 18:
#         return True
#     else:
#         return False
#
# print(police(14))