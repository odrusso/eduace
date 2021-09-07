const BASE_URL = process.env.API_HOST

export const get = (url: string): Promise<Response> => {
    return fetch(BASE_URL + url)
}

export const post = (url: string, body: unknown): Promise<Response> => {
    return fetch(BASE_URL + url, {
        method: "POST",
        body: JSON.stringify(body)
    })
}
