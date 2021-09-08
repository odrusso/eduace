import React from "react";
import {render, screen} from "@testing-library/react";
import {SolutionEntry} from "../Question";

describe("Solution input tests", () => {
    it("can enter maths and we get a good latex result", async () => {
        const {rerender} = render(<SolutionEntry latex={""} setLatex={jest.fn()}/>)
        await screen.findByRole("textbox")
        // It's unfortunate we have to control this with the internal state
        rerender(<SolutionEntry latex={"\\frac{1}{2}"} setLatex={jest.fn()}/>)
        await screen.findByText("output: \\frac{1}{2}")
    })
})
