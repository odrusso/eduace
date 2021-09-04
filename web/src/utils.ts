export const BASE_URL = process?.env?.NODE_ENV ? "http://localhost:3000" : ""

export const get = (url: string): Promise<Response> => {
    return fetch(BASE_URL + url)
}
