import {screen} from "@testing-library/react";
import {renderAppWithRoute} from "./utils";
import userEvent from "@testing-library/user-event";

describe("application tests", () => {
    it("shows question page on question route", async () => {
        renderAppWithRoute("/question")
        await screen.findByText("Question")
    })

    it("clicking link on home page takes you to question page", async () => {
        renderAppWithRoute("/")
        await screen.findByText("Go to question page")
        userEvent.click(screen.getByText("Go to question page"))
        await screen.findByText("Question")
    })
})
