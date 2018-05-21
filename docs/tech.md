# Technology and Engineering guide

This document shuold describe the interactions between the different components, languages, and platforms involved in the Eduace ecosystem.

## Brief

1. **API** *Python*
API Framework written in Python, using SymPy as mathematical backend, MongoDB for large scale storage. This stage includes:
    - Generation of questions
    - Generation of answers
    - Evaluation of answers
    - Generation of practice exams

    Future; the API will record information from exam entries and use in Machine Learning.

2. **Web/Admin Backend** *Flask / MongoDB*
The web and administration backend runs on Flask for hosting, and MongoDB for databasing. This stage includes:
    - Creation, deletion, modification, and storage of;
        - Users
        - Institutes
    - Secure logins and logouts
    - Error logging
    - Metric logging and access
    - Web-hosting
    - Accessing and calling API functions

3. **Web Frontend** *HTTP / AngularJS*
The Web Frontend is the 'website' that users expirence. This stage includes:
    - Desktop and Mobile compatibility
    - Landing Page
        - User Login
    - User dashboards
        - Mastery scores
        - Modification of user data
    - Institutional dashboards
        - Student progress
        - Adding, viewing, and deleting students
        - Viewing and changing liscencing (pricing, duration, etc)
    - Course dashboards
        - Tree of learning
        - Access to quizzes and learning
        - Progress indication
        - Generation of exams and answers
    - Pre-quiz
        - Choice of type of quiz
            - Exam conditions (emulated NCEA exam style paper)
            - Repetition (question-by-question feedback, only access to hints)
            - Learning (question-by-question feedback, full help access)
    - Quiz
        - Display of question
        - Natural mathematical input of answer
        - Hint hover-over
        - Step-by-step answer guide
    - Post-quiz
        - Review of performance
        - Analysis of weak points, suggested next steps