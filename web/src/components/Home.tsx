import React from "react"
import {Link} from "react-router-dom";

export const Home = (): JSX.Element => {
    return (
        <>
            <Link to="/question">Go to question page</Link>
            <h1>Welcome to the Eduace Beta!</h1>
            <p>Hold tight! We&apos;re still getting things up and running 😎</p>
        </>
    )
}
