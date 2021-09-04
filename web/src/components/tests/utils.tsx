import React from "react";
import {render} from "@testing-library/react";
import {App} from "../App";
import {MemoryRouter} from "react-router";

export const renderWithRoute = (component: JSX.Element, route = "/"): void => {
    render(
        <MemoryRouter initialEntries={[route]}>
            {component}
        </MemoryRouter>
    )
}

export const renderAppWithRoute = (route = "/"): void => {
    renderWithRoute(<App/>, route)
}
