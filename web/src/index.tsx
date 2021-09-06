import React from "react";
import {render} from "react-dom";
import {App} from "./components/App";
import {BrowserRouter} from "react-router-dom";

// Start the mocking conditionally.
if (process.env.MOCK_API === "true") {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
  require('./mocks/browser').worker.start()
}

render(<BrowserRouter><App/></BrowserRouter>, document.getElementById("root"))
