import katex from "katex";
import React, {ChangeEvent, useEffect, useRef, useState} from "react";
import {get, post} from "../utils";
import {MathfieldComponent} from "./MathliveComponent";
import {MathfieldElement} from "mathlive";

export const Question = (): JSX.Element => {
    const [questions, setQuestions] = useState<QuestionListResponseDTO | undefined>()
    const [selectedQuestion, setSelectedQuestion] = useState<QuestionRequestDTO | undefined>()
    const [selectedQuestionData, setSelectedQuestionData] = useState<QuestionResponseDTO | undefined>()
    const [latex, setLatex] = useState("")
    const latexDiv = useRef<HTMLDivElement>(null)

    const handleSubmit = async () => {
        // TODO: Disable button while submitting
        const url = `/api/v1/questions/${selectedQuestion?.type}/${selectedQuestion?.id}`
        const res = await post(url, {
            attempt: latex,
            question: selectedQuestionData!.question
        } as QuestionAnswerRequestDTO)
        const resBody = (await res.json()) as QuestionAnswerResponseDTO
        alert(`correct: ${resBody.result}`)
    }

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
            const url = `/api/v1/questions/${selectedQuestion.type}/${selectedQuestion.id}?seed=${seed}`

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
            {selectedQuestion && (
                <>
                    <div ref={latexDiv} data-testid={"question-latex"}/>
                    <SolutionEntry latex={latex} setLatex={setLatex}/>
                    <button onClick={handleSubmit}>Submit</button>
                </>
            )}
        </div>
    )
}

// TODO: Refactor these into a separate files
type QuestionPickerProps =
{
    questions: QuestionListResponseDTO,
        setSelectedQuestion
:
    (q: QuestionRequestDTO) => void
}

const QuestionPicker = (
{
    questions, setSelectedQuestion
}
: QuestionPickerProps): JSX.Element =>
{
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

export type SolutionEntry =
{
    latex: string,
        setLatex
:
    (latex: string) => void
}

export const SolutionEntry = (
{
    latex, setLatex
}
:SolutionEntry): JSX.Element =>
{
    const [mathfield, setMathfield] = useState<MathfieldElement | undefined>()

    useEffect(() => {
        if (!mathfield) return
        mathfield.style.border = "1px solid rgba(0, 0, 0, .3)"
        mathfield.style.borderRadius = "5px"
        mathfield.style.boxShadow = "0 0 8px rgba(0, 0, 0, .2)"
        mathfield.style.padding = "8px"
    }, [mathfield])

    return (
        <>
            <MathfieldComponent
                latex={latex}
                onChange={setLatex}
                mathfieldRef={(mf) => setMathfield(mf)}
            />

            <p>output: {latex}</p>
        </>
    )
}