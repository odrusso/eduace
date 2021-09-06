import katex from "katex";
import React, {ChangeEvent, useEffect, useRef, useState} from "react";
import {get} from "../utils";

export const Question = (): JSX.Element => {
    const [questions, setQuestions] = useState<QuestionListResponseDTO | undefined>()
    const [selectedQuestion, setSelectedQuestion] = useState<QuestionRequestDTO | undefined>()
    const [selectedQuestionData, setSelectedQuestionData] = useState<QuestionResponseDTO | undefined>()
    const latexDiv = useRef<HTMLDivElement>(null)

    // TODO: Think about this.
    const seed = "12345"

    // Run only on initial render
    useEffect(() => {
        const fetchQuestions = async () => {
            const url = `/api/v1/questions`
            const fetchResult = await get(url)
            if (fetchResult.status !== 200) {
                console.error(`Invalid response code ${fetchResult.status}`)
                return
            }
            const questionJson = await fetchResult.json()
            setQuestions(questionJson)
        }

        fetchQuestions();
    }, [])

    // Fetch the question every time the selectedQuestion changes
    useEffect(() => {
        if (!selectedQuestion) return
        const fetchData = async () => {
            // TODO: Better (centralised) URL construction
            const url = `/api/v1/question/${selectedQuestion.type}/${selectedQuestion.id}?seed=${seed}`

            const fetchResult = await get(url)
            if (fetchResult.status !== 200) {
                // TODO: Better error handling
                console.error(`Invalid response code ${fetchResult.status}`)
                return
            }
            const questionJson: QuestionResponseDTO = await fetchResult.json()
            setSelectedQuestionData(questionJson)
            katex.render(questionJson.question, latexDiv.current!)
        }

        fetchData();
    }, [selectedQuestion])

    if (!questions) return <h1>Loading...</h1>

    return (
        <div>
            <h1>Question page</h1>
            <h2>Mode: {process.env.NODE_ENV}</h2>
            <QuestionPicker questions={questions} setSelectedQuestion={setSelectedQuestion}/>
            <p>current seed: {seed}</p>
            <p>selected question: {selectedQuestion?.type} {selectedQuestion?.id}</p>
            <p>selected question data: {JSON.stringify(selectedQuestionData)}</p>
            <div ref={latexDiv} data-testid={"question-latex"}/>
        </div>
    )
}

// TODO: Refactor the picker into a separate file
type QuestionPickerProps = {
    questions: QuestionListResponseDTO,
    setSelectedQuestion: (q: QuestionRequestDTO) => void
}

const QuestionPicker = ({questions, setSelectedQuestion}: QuestionPickerProps): JSX.Element => {
    const questionToRender = questions.questions
        .filter((it) => it.questionTypeName === "mcat")
        .flatMap((question) => {
            return question.questionIds.map((id): QuestionRequestDTO => {
                return {
                    type: question.questionTypeName,
                    id: id
                }
            })
        })

    const handleChange = (e: ChangeEvent<HTMLSelectElement>) => {
        if (e.target.value === "off") return
        setSelectedQuestion(questionToRender[Number(e.target.value)])
    }

    return (
        <select onChange={handleChange} defaultValue={"off"}>
            <option disabled value={"off"}> -- select an option --</option>
            {questionToRender.map((question, index) =>
                <option key={index} value={index}>{question.type} {question.id}</option>
            )}
        </select>
    )
}
