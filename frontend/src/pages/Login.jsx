import styled from "styled-components";
import React, { useState, useEffect } from 'react';
import {mobile} from "../responsive";
import { fetchAccessToken, setAccessToken, fetchRefreshToken, setRefreshToken, setUserName, fetchUserName} from "../auth";
import TextField from '@mui/material/TextField';
import { useNavigate } from "react-router";
import axios from "axios";

const Container = styled.div`
  width: 100vw;
  height: 100vh;
  background: linear-gradient(
      rgba(255, 255, 255, 0.5),
      rgba(255, 255, 255, 0.5)
    ),
      center;
  background-size: cover;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const Wrapper = styled.div`
  width: 25%;
  padding: 20px;
  background-color: white;
  ${mobile({ width: "75%" })}
`;

const Title = styled.h1`
  font-size: 24px;
  font-weight: 300;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
`;

const Input = styled.input`
  flex: 1;
  min-width: 40%;
  margin: 10px 0;
  padding: 10px;
`;

const Button = styled.button`
  width: 40%;
  border: none;
  padding: 15px 20px;
  background-color: teal;
  color: white;
  cursor: pointer;
  margin-bottom: 10px;
`;

const Link = styled.a`
  margin: 5px 0px;
  font-size: 12px;
  text-decoration: underline;
  cursor: pointer;
`;

const Login = () => {

  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  let handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if ((email == "") & (password == "")) {
        return;
      } else {
        // make api call to our backend. we'll leave thisfor later
        axios.post("http://0.0.0.0:8000/user/login", 
        new URLSearchParams({
            'grant_type': '',
            'username': email,
            'password': password,
            'scope': '',
            'client_id': '',
            'client_secret': '',
          }),{
            headers: {
            'accept': 'application/json',
          }}).then(function (response) {
            console.log(response.data.access_token, "response.data.access_token");
            console.log(response.data.refresh_token, "response.data.refresh_token");
            if (response.data.access_token) {
              setAccessToken(response.data.access_token);
              setRefreshToken(response.data.refresh_token);
              navigate("/Profile");
            }
          })
          .catch(function (error) {
            console.log(error, "error");
          });
      }
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <Container style={{ "background-color": "#D2EBCD"}}>
      <Wrapper className="square border border-dark">
        <Title>SIGN IN</Title>
        <Form onSubmit={handleSubmit}>
          <TextField id="email" label="Email" value={email}
                      onChange={(e) => setEmail(e.target.value)} variant="outlined" className='mb-4' />
          <TextField id="password" label="Password" variant="outlined" value={password}
                      onChange={(e) => setPassword(e.target.value)} type='password' className='mb-4' />
          <Button>LOGIN</Button>
          <Link>DO NOT YOU REMEMBER THE PASSWORD?</Link>
          <Link>CREATE A NEW ACCOUNT</Link>
        </Form>
      </Wrapper>
    </Container>
  );
};

export default Login;