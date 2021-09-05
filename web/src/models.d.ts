type QuestionRequestDTO = {
    type: string,
    id: string,
    seed?: string
}

type QuestionResponseDTO = {
    description: string,
    question: string
}

type QuestionListResponseDTO = {
    questions: {
        questionTypeName: string,
        questionIds: string[]
    }[]
}

type QuestionAnswerRequestDTO = {
    attempt: string,
    question: string
}

type QuestionAnswerResponseDTO = {
    result: boolean
}
