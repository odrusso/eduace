const BASE_URL = process.env.API_HOST

export const get = (url: string): Promise<Response> => {
    return fetch(BASE_URL + url)
}
