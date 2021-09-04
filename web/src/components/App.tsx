import React from "react"
import {Route, Switch} from "react-router-dom";
import {Question} from "./Question";
import {Home} from "./Home";

export const App = (): JSX.Element => {
    return (
        <Switch>
            <Route exact path="/" component={Home}/>
            <Route exact path="/question" component={Question}/>
        </Switch>
    )
}
