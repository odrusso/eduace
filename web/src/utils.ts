// TODO: This will not work outside of mocked mode
// const BASE_URL = process?.env?.NODE_ENV ? "http://localhost:3000" : ""
const BASE_URL = "http://localhost:3000"

export const get = (url: string): Promise<Response> => {
    return fetch(BASE_URL + url)
}
