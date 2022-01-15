import katex from "katex";
import React, {ChangeEvent, useEffect, useRef, useState} from "react";
import {get, post, getRandomInteger} from "../utils";
import {MathfieldComponent} from "./MathliveComponent";
import {MathfieldElement} from "mathlive";
import "./Question.scss"
import {Button, FormControl, InputLabel, MenuItem, Select} from "@material-ui/core";
import JSConfetti from "js-confetti";

const happyEmojis = ['✅', '✅', '📚', '✖', '️➕', '➗']
const sadEmojis = ['❌', '❌', '😨', '🤔']

export const Question = (): JSX.Element => {
    const [questions, setQuestions] = useState<QuestionListResponseDTO | undefined>()
    const [selectedQuestion, setSelectedQuestion] = useState<QuestionRequestDTO | undefined>()
    const [selectedQuestionData, setSelectedQuestionData] = useState<QuestionResponseDTO | undefined>()
    const [latex, setLatex] = useState<string>("")
    const latexDiv = useRef<HTMLDivElement>(null)
    const [mathfield, setMathfield] = useState<MathfieldElement | undefined>()
    const [seed, setSeed] = useState<number>(getRandomInteger())
    const [confetti] = useState(new JSConfetti())


    const handleSubmit = async () => {
        const url = `/api/v1/question/${selectedQuestion?.type}/${selectedQuestion?.id}`
        const res = await post(url, {
            attempt: latex,
            question: selectedQuestionData!.question,
            seed: seed
        } as QuestionAnswerRequestDTO)
        const resBody = (await res.json()) as QuestionAnswerResponseDTO
        confetti.addConfetti({
            emojis: resBody.result ? happyEmojis : sadEmojis
        })
    }

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

        const fetchQuestion = async (selectedQuestion) => {
            const url = `/api/v1/question/${selectedQuestion.type}/${selectedQuestion.id}?seed=${seed}`

            const fetchResult = await get(url)
            if (fetchResult.status !== 200) {
                console.error(`Invalid response code ${fetchResult.status}`)
                return
            }
            const questionJson: QuestionResponseDTO = await fetchResult.json()
            setSelectedQuestionData(questionJson)

            setLatex("")
        }

        fetchQuestion(selectedQuestion)
    }, [selectedQuestion, seed])

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

    const buttonDisabled = mathfield?.getValue().includes("placeholder") ?? false

    return (
        <div className={"eduace-question-container"}>
            <QuestionPicker
                questions={questions}
                selectedQuestion={selectedQuestion}
                setSelectedQuestion={setSelectedQuestion}
            />
            {selectedQuestionData && (
                <>
                    <div className={"eduace-question-display"}>
                        <div ref={latexDiv} data-testid={"question-latex"}/>
                    </div>
                    <SolutionEntry
                        latex={latex}
                        setLatex={setLatex}
                        mathfield={mathfield}
                        setMathfield={setMathfield}
                    />
                    <div className={"eduace-submit-buttons"}>
                        <div className={"eduace-button-submit"}>
                            <Button
                                onClick={handleSubmit}
                                variant={"outlined"}
                                disableElevation={true}
                                disabled={buttonDisabled}
                            >
                                Submit
                            </Button>
                        </div>
                        <div className={"eduace-button-regen"}>
                            <Button
                                onClick={() => {
                                    setSeed(getRandomInteger())
                                }}
                                variant={"outlined"}
                                disableElevation={true}
                            >
                                Another!
                            </Button>
                        </div>
                    </div>
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

    const handleChange = (e: ChangeEvent<HTMLSelectElement>) => {
        if (e.target.value === "off") return

        const newQuestion = questions.questions[Number(e.target.value)]

        setSelectedQuestion({
            type: newQuestion!.typeName,
            id: newQuestion!.id,
            seed: undefined
        })

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
                {questions.questions.map((question, index) =>
                    <MenuItem key={index}
                              value={index}>{question.typeName} {question.id} - {question.description}</MenuItem>
                )}
            </Select>
        </FormControl>
    )
}

export type SolutionEntry = {
    latex: string,
    setLatex: (latex: string) => void,
    mathfield?: MathfieldElement
    setMathfield: (v: MathfieldElement) => void
}

export const SolutionEntry = ({latex, setLatex, mathfield, setMathfield}: SolutionEntry): JSX.Element => {
    // TODO: Add a prop to Mathfield component to take in these styles
    // and maybe any other default HTMLElement props?
    useEffect(() => {
        if (!mathfield) return
        mathfield.style.border = "1px solid rgba(0, 0, 0, .3)"
        mathfield.style.borderRadius = "1em"
        mathfield.style.padding = "1.5em"
        mathfield.style.backgroundColor = "white"
        mathfield.style.marginBottom = "2em"
    }, [mathfield])

    return (
        <div>
            <MathfieldComponent
                latex={latex}
                onChange={setLatex}
                mathfieldRef={(mf) => setMathfield(mf)}
            />
        </div>
    )
}
