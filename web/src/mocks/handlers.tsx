// We want to specify APIs exactly in every test, so we default to 500'ing everywhere
import {rest} from "msw";

export const handlers = [
    rest.get('*/api/v1/question/:questionType/:questionID', (req, res, ctx) => {
        return res(
            ctx.status(200),
            ctx.json({
                description: "Solve a linear equation.",
                question: `a x + b = ${req.params['questionID']} + \\frac12`
            } as QuestionResponseDTO)
        )
    }),

    rest.post('*/api/v1/question/:questionType/:questionID', (req, res, ctx) => {
        return res(
            ctx.status(200),
            ctx.json({
                result: req.params["questionID"] == "1",
            } as QuestionAnswerResponseDTO)
        )
    }),

    rest.get('*/api/v1/questions', (req, res, ctx) => {
        return res(
            ctx.status(200),
            ctx.json({
                questions: [{
                    questionTypeName: "mcat",
                    questionIds: ["1", "2", "3"]
                }]
            } as QuestionListResponseDTO)
        )
    })
]
