import React from "React"
import {App} from "../App";
import {render} from "@testing-library/react";
import {screen} from "@testing-library/react";

describe("application tests", () => {
    it("shows expected header text", async () => {
        render(<App/>)
        expect(await screen.findByText("hello world!")).toBeInTheDocument()
    })
})
