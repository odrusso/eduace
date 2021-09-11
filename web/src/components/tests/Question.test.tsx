import {renderAppWithRoute} from "./utils";
import {screen, waitFor} from "@testing-library/react";
import userEvent from "@testing-library/user-event";


describe("question page", () => {
    it("shows loading page and renders initially with no data", async () => {
        renderAppWithRoute("/question")
        await screen.findByText("Loading...")
        await screen.findByText("Question page")
        await screen.findByText("selected question:")
    })

    it("question data is hidden before quesiton selected", async () => {
        renderAppWithRoute("/question")
        await screen.findByText("selected question:")
        expect(screen.queryByTestId("question-latex")).not.toBeInTheDocument()
        expect(screen.queryByText("Submit")).not.toBeInTheDocument()
        const selectBox = screen.getByLabelText("Question")
        await userEvent.click(selectBox)
        await userEvent.click(await screen.findByText("mcat 1"))
        await screen.findByText("selected question: mcat 1")
        expect(await screen.findByTestId("question-latex")).toBeInTheDocument()
        expect(screen.getByText("Submit")).toBeInTheDocument()
    })

    it("can select a question and data loads and renders latex", async () => {
        renderAppWithRoute("/question")
        await screen.findByText("selected question:")
        const selectBox = screen.getByLabelText("Question")
        await userEvent.click(selectBox)
        await userEvent.click(await screen.findByText("mcat 1"))
        await screen.findByText("selected question: mcat 1")
        await waitFor(() => expect(screen.getByTestId("question-latex").children.length).not.toBe(0))
    })

    it("loads list of questions from API", async () => {
        renderAppWithRoute("/question")
        await screen.findByText("selected question:")
        const selectBox = screen.getByLabelText("Question")
        await userEvent.click(selectBox)
        await screen.findByText("mcat 1")
        screen.getByText("mcat 2")
        screen.getByText("mcat 3")
    })
})
