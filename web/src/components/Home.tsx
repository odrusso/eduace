import React from "react"
import {Link} from "react-router-dom";

export const Home = (): JSX.Element => {
    return (
        <Link to="/question">Go to question page</Link>
    )
}
