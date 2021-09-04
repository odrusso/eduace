import { setupServer } from 'msw/node'
import { rest } from 'msw'

// We want to specify APIs exactly in every test, so we default to 500'ing everywhere
const handlers = [
    rest.post('*', (req, res, ctx) => {
        console.error(`No mock setup for ${req.url}`)
        return res(
            ctx.status(500)
        )
    })
]

// Setup requests interception using the given handlers.
export const server = setupServer(...handlers)
