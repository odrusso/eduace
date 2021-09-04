import {fireEvent, screen} from "@testing-library/react";
import {renderAppWithRoute} from "./utils";

describe("application tests", () => {
    it("shows question page on question route", async () => {
        renderAppWithRoute("/question")
        expect(await screen.findByText(/Question/)).toBeInTheDocument()
    })

    it("clicking link on home page takes you to question page", async () => {
        renderAppWithRoute("/")
        expect(await screen.findByText("Go to question page")).toBeInTheDocument()
        fireEvent.click(screen.getByText("Go to question page"))
        expect(await screen.findByText("Question page")).toBeInTheDocument()
    })
})
