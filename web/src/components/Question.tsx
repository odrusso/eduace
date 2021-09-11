import katex from "katex";
import React, {ChangeEvent, useEffect, useRef, useState} from "react";
import {get, post} from "../utils";
import {MathfieldComponent} from "./MathliveComponent";
import {MathfieldElement} from "mathlive";
import "./Question.scss"
import {Button, FormControl, InputLabel, MenuItem, Select} from "@material-ui/core";

export const Question = (): JSX.Element => {
    const [questions, setQuestions] = useState<QuestionListResponseDTO | undefined>()
    const [selectedQuestion, setSelectedQuestion] = useState<QuestionRequestDTO | undefined>()
    const [selectedQuestionData, setSelectedQuestionData] = useState<QuestionResponseDTO | undefined>()
    const [latex, setLatex] = useState("")
    const latexDiv = useRef<HTMLDivElement>(null)

    const handleSubmit = async () => {
        // TODO: Disable button while submitting
        const url = `/api/v1/question/${selectedQuestion?.type}/${selectedQuestion?.id}`
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
            const url = `/api/v1/question/${selectedQuestion.type}/${selectedQuestion.id}?seed=${seed}`

            const fetchResult = await get(url)
            if (fetchResult.status !== 200) {
                // TODO: Better error handling
                console.error(`Invalid response code ${fetchResult.status}`)
                return
            }
            const questionJson: QuestionResponseDTO = await fetchResult.json()
            setSelectedQuestionData(questionJson)
        }

        fetchData();
    }, [selectedQuestion])


    // Updates the latex
    useEffect(() => {
        // There can be a race condition where the selectedQuestionData is returned
        // before the ref is assigned to the DOM element. So we have to have
        // both as deps here, and be careful about what we do when either of the change
        if (!selectedQuestionData) return
        if (latexDiv.current === null) return
        katex.render(selectedQuestionData.question, latexDiv.current!, {displayMode: true})
    }, [selectedQuestionData, latexDiv])

    if (!questions) return <div className={"eduace-question-container"}><h1>Loading...</h1></div>

    return (
        <div className={"eduace-question-container"}>
            <h1>Question page</h1>
            <QuestionPicker
                questions={questions}
                selectedQuestion={selectedQuestion}
                setSelectedQuestion={setSelectedQuestion}
            />
            <p>selected question: {selectedQuestion?.type} {selectedQuestion?.id}</p>
            <p>selected question data: {JSON.stringify(selectedQuestionData)}</p>
            {selectedQuestionData && (
                <>
                    <div className={"eduace-question-display"}>
                        <div ref={latexDiv} data-testid={"question-latex"}/>
                    </div>
                    <SolutionEntry latex={latex} setLatex={setLatex}/>
                    <Button onClick={handleSubmit} variant="contained" disableElevation={true}>
                        Submit
                    </Button>
                </>
            )}
        </div>
    )
}

// TODO: Refactor these into a separate files
type QuestionPickerProps = {
    questions: QuestionListResponseDTO,
    selectedQuestion?: QuestionRequestDTO,
    setSelectedQuestion: (q: QuestionRequestDTO) => void
}

const QuestionPicker = ({questions, selectedQuestion, setSelectedQuestion}: QuestionPickerProps): JSX.Element => {
    const [index, setIndex] = useState<string>("")

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
        setIndex(e.target.value)
    }

    return (
        <FormControl variant="outlined">
            <InputLabel id="eduace-question-selector-label">Question</InputLabel>
            <Select
                onChange={handleChange}
                labelId={'eduace-question-selector-label'}
                style={{minWidth: '12em'}}
                label={'question'}
                value={index}
            >
                {questionToRender.map((question, index) =>
                    <MenuItem key={index} value={index}>{question.type} {question.id}</MenuItem>
                )}
            </Select>
        </FormControl>
    )
}

export type SolutionEntry = {
    latex: string,
    setLatex: (latex: string) => void
}

export const SolutionEntry = ({latex, setLatex}: SolutionEntry): JSX.Element => {
    const [mathfield, setMathfield] = useState<MathfieldElement | undefined>()

    // TODO: Add a prop to Mathfield component to take in these styles
    // and maybe any other default HTMLElement props?
    useEffect(() => {
        if (!mathfield) return
        mathfield.style.border = "1px solid rgba(0, 0, 0, .3)"
        mathfield.style.borderRadius = "5px"
        mathfield.style.boxShadow = "0 0 8px rgba(0, 0, 0, .2)"
        mathfield.style.padding = "8px"
    }, [mathfield])

    return (
        <div>
            <MathfieldComponent
                latex={latex}
                onChange={setLatex}
                mathfieldRef={(mf) => setMathfield(mf)}
            />

            <p>output: {latex}</p>
        </div>
    )
}