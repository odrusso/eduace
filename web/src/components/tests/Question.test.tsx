import {renderAppWithRoute} from "./utils";
import {screen, waitFor} from "@testing-library/react";
import userEvent from "@testing-library/user-event";


describe("question page", () => {
    it("shows loading page and renders initially with no data", async () => {
        renderAppWithRoute("/question")
        await screen.findByText("Loading...")
        await screen.findByText("Question")
    })

    it("question data is hidden before quesiton selected", async () => {
        renderAppWithRoute("/question")
        expect(screen.queryByTestId("question-latex")).not.toBeInTheDocument()
        expect(screen.queryByText("Submit")).not.toBeInTheDocument()
        const selectBox = await screen.findByLabelText("Question")
        await userEvent.click(selectBox)
        await userEvent.click(await screen.findByText("mcat 1 - solve a linear system."))
        expect(await screen.findByTestId("question-latex")).toBeInTheDocument()
        expect(screen.getByText("Submit")).toBeInTheDocument()
    })

    it("can select a question and data loads and renders latex", async () => {
        renderAppWithRoute("/question")
        const selectBox = await screen.findByLabelText("Question")
        await userEvent.click(selectBox)
        await userEvent.click(await screen.findByText("mcat 1 - solve a linear system."))
        await waitFor(() => expect(screen.getByTestId("question-latex").children.length).not.toBe(0))
    })

    it("loads list of questions from API", async () => {
        renderAppWithRoute("/question")
        const selectBox = await screen.findByLabelText("Question")
        await userEvent.click(selectBox)
        await screen.findByText("mcat 1 - solve a linear system.")
        screen.getByText("mcat 2 - solve a non linear system.")
    })
})
