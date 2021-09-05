// We want to specify APIs exactly in every test, so we default to 500'ing everywhere
import {rest} from "msw";

export const handlers = [
    rest.post('*', (req, res, ctx) => {
        console.error(`No mock setup for ${req.url}`)
        return res(
            ctx.status(500)
        )
    }),

    rest.get('*/api/v1/questions/:questionType/:questionID', (req, res, ctx) => {
        return res(
            ctx.status(200),
            ctx.json({
                description: "Solve a linear equation.",
                question: `a x + b = ${req.params['questionID']} + \\frac12`
            } as QuestionResponseDTO)
        )
    }),

    rest.post('*/api/v1/questions/:questionType/:questionID', (req, res, ctx) => {
        console.log(req.body)
        return res(
            ctx.status(200),
            ctx.json({
                result: req.params["questionID"] == "0"
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
