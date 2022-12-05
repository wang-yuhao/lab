import { useLocation,Navigate } from "react-router-dom"

export const setAccessToken = (token)=>{
    localStorage.setItem('UserAccessToken', token)// make up your own token
}

export const setRefreshToken = (token)=>{
    localStorage.setItem('UserRefreshToken', token)
}

export const setUserName = (name)=>{
    localStorage.setItem('UserName', name)// make up your own token
}

export const setUserRole = (role)=>{
    return localStorage.setItem('Role', role)
}

export const fetchAccessToken = ()=>{
    return localStorage.getItem('UserAccessToken')
}

export const fetchRefreshToken = ()=>{
    return localStorage.getItem('UserRefreshToken')
}

export const fetchUserName = ()=>{
    return localStorage.getItem('UserName')
}

export const fetchUserRole = ()=>{
    return localStorage.getItem('Role')
}

export function RequireToken({children}){
    let username = fetchUserName()
    let auth = fetchAccessToken()
    let location = useLocation()

    if(!username || !auth){

        return <Navigate to='/' state ={{from : location}}/>;
    }

    return children;
}
