import React from "react"
import {Route, Switch} from "react-router-dom";
import {Question} from "./Question";
import {Home} from "./Home";
import "./App.scss"
import logo from '../public/logo.png';

export const App = (): JSX.Element => {
    return (
        <div className={"eduace-app-container"}>
            <Sidebar/>
            <Switch>
                <Route exact path="/" component={Home}/>
                <Route exact path="/question" component={Question}/>
            </Switch>
        </div>
    )
}

export const Sidebar = (): JSX.Element => {
    return (
        <div className={"eduace-app-sidebar"}>
            <img src={logo} alt={"eduace logo"} className={"eduace-sidebar-logo"}/>
        </div>
    )
}
