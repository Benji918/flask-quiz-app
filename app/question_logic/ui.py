from app.question_logic.quiz_brain import QuizBrain


class Quizinterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.score = None
        self.text = None
        self.color = None
        self.quiz = quiz_brain

    def anwser_true(self) -> str:
        q_anwser = 'True'
        return self.give_feedback(self.quiz.check_answer(q_anwser))

    def anwser_false(self) -> str:
        q_anwser = 'False'
        return self.give_feedback(self.quiz.check_answer(q_anwser))

    def get_question(self):
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            return q_text
        else:
            return False

    # def next_question(self):
    #     if self.quiz.still_has_questions():
    #         next_question = self.quiz.next_question()
    #         self.score = f'Score:{self.quiz.score}'
    #     else:
    #         return False

    def give_feedback(self, is_right: bool) -> str:
        if is_right:
            self.color = 'green'
            return self.color
        else:
            self.color = 'red'
            return self.color

    def refresh(self):
        self.quiz.reset()
        # self.score.config(text=f'Score:{self.quiz.score}')
        # q_text = self.quiz.next_question()
        # self.canvas.itemconfig(self.question_text, text=q_text)
