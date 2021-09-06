const BASE_URL = process.env.BASE_URL

export const get = (url: string): Promise<Response> => {
    return fetch(BASE_URL + url)
}
