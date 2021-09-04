import React, {ChangeEvent, useEffect, useState} from "react";
import {get} from "../utils";

export const Question = (): JSX.Element => {

    // TODO: Pull this dynamically from API
    const listOfQuestions: QuestionRequestDTO[] = [
        {type: "mcat", id: "1"},
        {type: "mcat", id: "2"},
        {type: "mcat", id: "3"},
    ]

    const [selectedQuestion, setSelectedQuestion] = useState<QuestionRequestDTO>(listOfQuestions[0])
    const [selectedQuestionData, setSelectedQuestionData] = useState<QuestionResponseDTO | undefined>()

    // TODO: Think about this.
    const seed = "12345"

    // Fetch the question every time the selectedQuestion changes
    useEffect(() => {
        const fetchData = async () => {
            // TODO: Better (centralised) URL construction
            const url = `/api/v1/questions/${selectedQuestion.type}/${selectedQuestion.id}?seed=${seed}`

            const fetchResult = await get(url)
            if (fetchResult.status !== 200) {
                // TODO: Better error handling
                console.error(`Invalid response code ${fetchResult.status}`)
                return
            }
            const questionJson = await fetchResult.json()
            setSelectedQuestionData(questionJson)
        }

        fetchData();
    }, [selectedQuestion])

    return (
        <div>
            <h1>Question page</h1>
            <h2>Mode: {process.env.NODE_ENV}</h2>
            <QuestionPicker questions={listOfQuestions} setSelectedQuestion={setSelectedQuestion}/>
            <p>current seed: {seed}</p>
            <p>selected question: {selectedQuestion.type} {selectedQuestion.id}</p>
            <p>selected question data: {JSON.stringify(selectedQuestionData)}</p>
        </div>
    )
}

// TODO: Refactor the picker into a separate file
type QuestionPickerProps = {
    questions: QuestionRequestDTO[],
    setSelectedQuestion: (q: QuestionRequestDTO) => void
}

const QuestionPicker = ({questions, setSelectedQuestion}: QuestionPickerProps): JSX.Element => {

    const handleChange = (e: ChangeEvent<HTMLSelectElement>) => {
        setSelectedQuestion(questions[e.target.value])
    }

    return (
        <select onChange={handleChange}>
            {questions.map((question, index) =>
                <option key={index} value={index}>{question.type} {question.id}</option>
            )}
        </select>
    )
}
