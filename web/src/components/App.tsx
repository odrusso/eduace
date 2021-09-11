import React from "react"
import {Route, Switch} from "react-router-dom";
import {Question} from "./Question";
import {Home} from "./Home";
import "./App.scss"
import logo from '../public/logo.png';

export const App = (): JSX.Element => {
    return (
        <EduacePage>
            <Switch>
                <Route exact path="/" component={Home}/>
                <Route exact path="/question" component={Question}/>
            </Switch>
        </EduacePage>
    )
}

type EduacePageProps = React.InputHTMLAttributes<HTMLDivElement>;

export const EduacePage = ({children}: EduacePageProps): JSX.Element => {
    return (
        <div className={'eduace-app-container'}>
            <Sidebar/>
            <div className={'eduace-content-container'}>
                <Header/>
                {children}
            </div>
        </div>
    )
}

export const Header = (): JSX.Element => {
    return (
        <div className={'eduace-header-container'}>
            <div className={'eduace-header-text'}>EDUACE</div>
        </div>
    )
}

export const Sidebar = (): JSX.Element => {
    return (
        <div className={"eduace-app-sidebar"}>
            <div className={"eduace-sidebar-logo-container"}>
                <img src={logo} alt={"eduace logo"} className={"eduace-sidebar-logo"}/>
            </div>
            <div className={"eduace-sidebar-navigation"}>
                <ul>
                    <li>Test</li>
                    <li>Test 2</li>
                </ul>
            </div>
        </div>
    )
}
