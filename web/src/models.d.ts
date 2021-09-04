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
    questionType: {
        questionTypeName: string,
        questionIds: string[]
    }[]
}
