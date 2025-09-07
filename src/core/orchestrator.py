# src/core/orchestrator.py

from src.agents.planner import get_planner_agent
from src.agents.content import get_content_agent
from src.agents.practice import get_practice_agent
from src.agents.evaluator import get_evaluator_agent
from src.agents.motivator import get_motivator_agent


class TutorOrchestrator:
    def __init__(self):
        self.planner_agent = get_planner_agent()
        self.content_agent = get_content_agent()
        self.practice_agent = get_practice_agent()
        self.evaluator_agent = get_evaluator_agent()
        self.motivator_agent = get_motivator_agent()

        self.main_topic = ""
        self.roadmap = []
        self.quiz_results = []

    def run(self, user_input: str):
        self.main_topic = user_input
        self.quiz_results = []

        roadmap_result = self.planner_agent.invoke({"user_input": user_input})
        self.roadmap = roadmap_result.get("roadmap", [])

        if not self.roadmap:
            yield {"type": "error", "data": "I couldn't create a study plan."}
            return

        yield {"type": "roadmap", "data": self.roadmap}

        for sub_topic in self.roadmap:
            explanation = self.content_agent.invoke({"sub_topic": sub_topic})
            yield {"type": "content", "data": {"topic": sub_topic, "explanation": explanation}}

            quiz_data = self.practice_agent.invoke({"sub_topic": sub_topic})
            questions = quiz_data.get("questions", [])

            for i, question_item in enumerate(questions):
                user_answer = yield {"type": "quiz", "data": {"question_item": question_item,
                                                              "progress": f"Question {i + 1}/{len(questions)}"}}

                evaluation_input = {
                    "question": question_item["question"],
                    "options": str(question_item["options"]),
                    "correct_answer": question_item["answer"],
                    "student_answer": user_answer
                }
                evaluation_result = self.evaluator_agent.invoke(evaluation_input)
                self.quiz_results.append(evaluation_result['correct'])
                yield {"type": "feedback", "data": evaluation_result}

        correct_answers = sum(1 for r in self.quiz_results if r)
        total_questions = len(self.quiz_results)
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

        summary = f"Quiz complete! You scored {correct_answers}/{total_questions} ({score:.2f}%)."

        if score < 75:
            motivation = self.motivator_agent.invoke({"topic": self.main_topic})
            summary += f"\n\n{motivation}"
            yield {"type": "final_summary", "data": {"summary": summary, "offer_retest": True, "score": score}}
        else:
            summary += "\n\nExcellent work! You have a solid grasp of this topic."
            yield {"type": "final_summary", "data": {"summary": summary, "offer_retest": False, "score": score}}

    def run_retest(self):
        """ A separate generator for handling the re-test loop. """
        self.quiz_results = []  # Reset results for the re-test
        yield {"type": "content", "data": {"topic": f"Re-Test: {self.main_topic}",
                                           "explanation": "Let's try that again! Here is a new set of questions on the whole topic."}}

        # For a re-test, we generate a comprehensive quiz on the main topic
        quiz_data = self.practice_agent.invoke({"sub_topic": self.main_topic})
        questions = quiz_data.get("questions", [])

        for i, question_item in enumerate(questions):
            user_answer = yield {"type": "quiz", "data": {"question_item": question_item,
                                                          "progress": f"Question {i + 1}/{len(questions)}"}}

            evaluation_input = {
                "question": question_item["question"], "options": str(question_item["options"]),
                "correct_answer": question_item["answer"], "student_answer": user_answer
            }
            evaluation_result = self.evaluator_agent.invoke(evaluation_input)
            self.quiz_results.append(evaluation_result['correct'])
            yield {"type": "feedback", "data": evaluation_result}

        correct_answers = sum(1 for r in self.quiz_results if r)
        total_questions = len(self.quiz_results)
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

        summary = f"Re-Test Complete! You scored {correct_answers}/{total_questions} ({score:.2f}%)."

        if score < 75:
            summary += "\n\nKeep practicing, you're making progress! Feel free to try another re-test or start a new topic."
            yield {"type": "final_summary", "data": {"summary": summary, "offer_retest": True, "score": score}}
        else:
            summary += "\n\nFantastic improvement! You've mastered it."
            yield {"type": "final_summary", "data": {"summary": summary, "offer_retest": False, "score": score}}
