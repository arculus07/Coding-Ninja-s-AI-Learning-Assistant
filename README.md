
---

# Coding Ninjas AI Tutor - A Multi-Agent Learning System

Developed by: **Ayush Ranjan**
[LinkedIn](https://www.linkedin.com/in/ayushxranjan/) | [GitHub](https://github.com/arculus07)

---

## Overview

The Coding Ninjas AI Tutor is a fully functional, adaptive learning platform built as part of the Coding Ninjas assignment.
It uses a multi-agent architecture powered by LangChain to deliver personalized, interactive, and structured lessons for any topic a learner wishes to explore.

Instead of being static and one-size-fits-all, this project simulates a team of AI experts working together to make learning dynamic, modular, and engaging.

---

## Problem Statement

### Challenges Learners Face

* Lack of a clear roadmap: Unsure where to start and what to learn next.
* Generic content: Explanations are not adaptive (for example, unnecessary code in theory topics).
* Passive learning: No way to instantly test comprehension.
* No personalized feedback: Learners don’t know why their answers are wrong.

### Our Solution: Multi-Agent System

* Specialization: Each agent focuses on a single role (Planner, Teacher, Quiz Master, etc.).
* Modularity: Easy to scale and maintain.
* Orchestration: Central controller ensures a smooth, stateful learning journey.

---

## System Architecture & Agents

The application is built with Streamlit and orchestrated via LangChain.

### Agents

1. Planner Agent (Curriculum Designer)

   * Input: User’s topic.
   * Task: Generate a structured learning roadmap.
   * Output: Sub-topics arranged as a visual timeline.

2. Content Agent (Teacher)

   * Input: A sub-topic.
   * Task: Deliver clear explanations, including code only for programming topics.
   * Output: Text explanation.

3. Practice Agent (Quiz Master)

   * Input: A sub-topic.
   * Task: Create four multiple-choice questions (easy to hard).
   * Output: JSON with structured quiz.

4. Evaluator Agent (Grader)

   * Input: User’s quiz answer.
   * Task: Judge correctness, provide hints or praise.
   * Output: JSON in the form `{"correct": boolean, "feedback": "..."}`.

5. Motivator Agent (Coach)

   * Input: Low score signal.
   * Task: Provide empathetic encouragement.
   * Output: Motivational message related to the topic.

---

## Tech Stack

* Language: Python
* AI Orchestration: LangChain
* LLM Integration: langchain-openai
* Frontend: Streamlit
* Environment Management: python-dotenv

---

## LLM Selection

* Chosen Model: gpt-4o-mini

  * Balanced in speed, cost, and reliability.
  * Strong instruction-following ensures stable structured JSON generation.

* Alternatives considered:

  * gpt-4o / gpt-5 → More expensive and slower.
  * gpt-5-nano → No temperature control, less creativity.
  * Google Gemma (Hugging Face Free Tier) → Produced frequent errors.

---

## Setup & Run Instructions

1. Clone the Repository:

```
git clone https://github.com/your-username/ai_tutor_project.git
cd ai_tutor_project
```

2. Create and Activate Virtual Environment:

```
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install Dependencies:

```
pip install -r requirements.txt
```

4. Set Up API Key:
   Create a `.env` file in the project root and add:

```
OPENAI_API_KEY="sk-..."
```

5. Run the Application:

```
streamlit run app.py
```

The app will now open in your browser.

---

## Acknowledgement

* Streamlit UI (frontend) was created with the assistance of Google Gemini.
* Multi-agent backend, system design, and orchestration were implemented by Ayush Ranjan.

---

## Example Use Case

1. User asks: “Teach me about Python Dictionaries.”
2. Planner Agent creates a roadmap → Introduction, Syntax, Operations, Use Cases.
3. Content Agent explains each sub-topic.
4. Practice Agent generates a quiz.
5. Evaluator Agent checks answers and provides feedback.
6. Motivator Agent encourages the learner if the score is low.

---

## Future Scope

* Add support for voice interaction.
* Integration with progress tracking dashboards.
* Expand to other domains like Math, History, and Science.

---

## Contact

Author: Ayush Ranjan
[LinkedIn](https://www.linkedin.com/in/ayushxranjan/) | [GitHub](https://github.com/arculus07)

---
