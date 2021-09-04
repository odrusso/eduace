import '@testing-library/jest-dom/extend-expect'
import {server} from './mocks/server'
import {toHaveNoViolations} from "jest-axe";

expect.extend(toHaveNoViolations)


// Node has no concept of fetch, so we polyfill here just to override immediately
// eslint-disable-next-line no-undef
window.fetch = require("node-fetch")

// eslint-disable-next-line no-undef
beforeAll(() => {
    // Enable the mocking in tests.
    server.listen()
})

// eslint-disable-next-line no-undef
afterEach(() => {
    // Reset any runtime handlers tests may use.
    server.resetHandlers()
})

// eslint-disable-next-line no-undef
afterAll(() => {
    // Clean up once the tests are done.
    server.close()
})
