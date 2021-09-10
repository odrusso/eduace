import React from "react"
import {Route, Switch} from "react-router-dom";
import {Question} from "./Question";
import {Home} from "./Home";
import "./App.scss"

export const App = (): JSX.Element => {
    return (
        <div className={"eduace-app-container"}>
            <div className={"eduace-app-sidebar"} />
            <Switch>
                <Route exact path="/" component={Home}/>
                <Route exact path="/question" component={Question}/>
            </Switch>
        </div>
    )
}
