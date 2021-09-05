import {renderAppWithRoute} from "./utils";
import {screen} from "@testing-library/react";
import userEvent from "@testing-library/user-event";


describe("question page", () => {
    it("shows loading page and renders initially with no data", async () => {
        renderAppWithRoute("/question")
        await screen.findByText("Loading...")
        await screen.findByText("Question page")
        await screen.findByText("selected question:")
    })

    it("can select a question and data loads", async () => {
        renderAppWithRoute("/question")
        await screen.findByText("selected question:")
        const selectBox = screen.getByText("-- select an option --")
        userEvent.selectOptions(selectBox.parentElement, ["0"])
        await screen.findByText("selected question: mcat 1")
    })

    it("loads list of questions from API", async () => {
        renderAppWithRoute("/question")
        await screen.findByText("selected question:")
        const selectBox = screen.getByText("-- select an option --")
        expect(selectBox.parentElement.children.length).toBe(4)
        screen.getByText("mcat 1")
        screen.getByText("mcat 2")
        screen.getByText("mcat 3")

    })
})
