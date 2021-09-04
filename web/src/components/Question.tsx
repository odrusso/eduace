import React, {ChangeEvent, useEffect, useState} from "react";

// TODO Refactor this into a models area
type QuestionTypeDTO = {
    type: string,
    id: string
}

export const Question = (): JSX.Element => {

    const listOfQuestions: QuestionTypeDTO[] = [
        {type: "mcat", id: "1"},
        {type: "mcat", id: "2"},
        {type: "mcat", id: "3"},
    ]

    const [selectedQuestion, setSelectedQuestion] = useState<QuestionTypeDTO>(listOfQuestions[0])
    // TODO: Type the API reqs and responses
    const [selectedQuestionData, setSelectedQuestionData] = useState<any | undefined>()

    // TODO: Think about this.
    const seed = "12345"

    // Fetch the question every time the selectedQuestion changes
    useEffect(() => {
        const fetchData = async () => {
            // TODO: Better (centralised) URL construction
            const url = `/api/v1/questions/${selectedQuestion.type}/${selectedQuestion.id}?seed=${seed}`

            // TODO: Actually fetch from the API
            console.log(`fetching from URL: ${url}`)
            const fetchResult = await fetch(url)
            if (fetchResult.status !== 200) {
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
    questions: QuestionTypeDTO[],
    setSelectedQuestion: (q: QuestionTypeDTO) => void
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
