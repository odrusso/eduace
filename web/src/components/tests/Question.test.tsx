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
        const selectBox = screen.getByText("-- select an option --")
        userEvent.selectOptions(selectBox.parentElement!, ["0"])
        await screen.findByText("selected question: mcat 1")
        expect(await screen.findByTestId("question-latex")).toBeInTheDocument()
        expect(screen.getByText("Submit")).toBeInTheDocument()
    })

    it("can select a question and data loads and renders latex", async () => {
        renderAppWithRoute("/question")
        await screen.findByText("selected question:")
        const selectBox = screen.getByText("-- select an option --")
        userEvent.selectOptions(selectBox.parentElement!, ["0"])
        await screen.findByText("selected question: mcat 1")
        await waitFor(() => expect(screen.getByTestId("question-latex").children.length).not.toBe(0))
    })

    it("loads list of questions from API", async () => {
        renderAppWithRoute("/question")
        await screen.findByText("selected question:")
        const selectBox = screen.getByText("-- select an option --")
        expect(selectBox.parentElement!.children!.length).toBe(4)
        screen.getByText("mcat 1")
        screen.getByText("mcat 2")
        screen.getByText("mcat 3")
    })

    it.skip("can enter maths and we get a good latex result", async () => {
        /**
         * For the life of me, I really can't get this to work.
         * It might be jsdom which doesn't like the object,
         * it might be RTL which can't interact with it.
         * Something about ShadowDOM. I'm stumped :/
         */
        // render(<SolutionEntry/>)
        // const mathFieldRoot = (await screen.findByRole("textbox")) as MathfieldElement
        // mathFieldRoot.setValue("\\frac{1}{2}")
        // await screen.findByText("output: \\frac{1}{2}")
    })
})
