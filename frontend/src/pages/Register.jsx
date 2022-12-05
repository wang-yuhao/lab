import React, { useState, useEffect } from 'react';
import styled from "styled-components";
import { mobile } from "../responsive";
import {
  MDBCardBody,
  MDBRow,
  MDBCol,
}
  from 'mdb-react-ui-kit';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import TextField from '@mui/material/TextField';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import Box from '@mui/material/Box';
import Autocomplete from '@mui/material/Autocomplete';
import Button from '@mui/material/Button';
import RefreshIcon from '@mui/icons-material/Refresh';
import SendIcon from '@mui/icons-material/Send';
import Stack from '@mui/material/Stack';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormLabel from '@mui/material/FormLabel';
import { useNavigate } from "react-router";
import { fetchAccessToken, setAccessToken, fetchRefreshToken, setRefreshToken, setUserName, fetchUserName } from "../auth";
import axios from "axios";
import Grid from '@mui/material/Unstable_Grid2'; // Grid version 2
import CssBaseline from '@mui/material/CssBaseline';
import Rightbar from '../components/Rightbar';
import Sidebar from '../components/Sidebar';

const MDBSelect = styled.div`
  width: 40%;
  padding: 20px;
  background-color: white;
  ${mobile({ width: "75%" })}
`;

function Register() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [gender, setGender] = useState("female");
  const [message, setMessage] = useState("");
  const [birthdate, setBirthdate] = useState("");
  const [password, setPassword] = useState("");
  const [country, setCountry] = useState("");
  const [ort, setOrt] = useState("");

  let handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if ((name == "") & (password == "")) {
        return;
      } else {
        // make api call to our backend. we'll leave thisfor later
        axios.post("http://0.0.0.0:8000/user/create_user", {
          'name': name,
          'email': email,
          'phone_number': phone,
          'gender': gender,
          'birth_date': birthdate,
          'country': country,
          'ort': ort,
          'password': password,
        }, {
          headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
          }
        }).then(function (response) {
          console.log(response.data.access_token, "response.data.access_token");
          console.log(response.data.refresh_token, "response.data.refresh_token");
          if (response.data.access_token) {
            setAccessToken(response.data.access_token);
            setRefreshToken(response.data.refresh_token);
            setUserName(name)
            navigate("/");
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
    <Box>
      <Stack direction="row" spacing={2} justifyContent="space-between">
        <Box>
          <List>
            <ListItem disablePadding>
              <ListItemButton component="a" href="/">
                <ListItemIcon>
                  <Home />
                </ListItemIcon>
                <ListItemText primary="Homepage" />
              </ListItemButton>
            </ListItem>
            <ListItem disablePadding>
              <ListItemButton component="a" href="/Login">
                <ListItemIcon>
                  <Person />
                </ListItemIcon>
                <ListItemText primary="Log In" />
              </ListItemButton>
            </ListItem>
          </List>
        </Box>
        <Box flex={4} p={2}>
          <Grid sx={{ flexGrow: 1 }} container spacing={2} justifyContent="center" alignItems="center">
            <Grid spacing={2} container justifyContent="center" alignItems="center" sx={{
              flexGrow: 1,
              bgcolor: 'background.paper',
              m: 2,
              p: 2,
              borderRadius: 2,
              width: '100%',
            }}>

              <Grid xs={12} className="pt-4 square bg-light">
                <Box>
                  <CssBaseline />
                  <Box className="mx-5">
                    <form onSubmit={handleSubmit}>
                      <MDBCardBody className='text-black d-flex flex-column justify-content-center'>
                        <h3 className="mb-5 text-uppercase fw-bold">Student registration form</h3>
                        <TextField id="name" label="Name" value={name}
                          onChange={(e) => setName(e.target.value)} variant="outlined" className='mb-4' />
                        <LocalizationProvider dateAdapter={AdapterDayjs} wrapperClass='mb-4'>
                          <DatePicker
                            disableFuture
                            label="Birth date"
                            openTo="year"
                            views={['year', 'month', 'day']}
                            value={birthdate}
                            onChange={(newValue) => {
                              setBirthdate(newValue);
                            }}
                            renderInput={(params) => <TextField {...params} />}></DatePicker>
                        </LocalizationProvider>

                        <FormLabel id="demo-row-radio-buttons-group-label" className='mt-4' >Gender</FormLabel>
                        <RadioGroup
                          row
                          aria-labelledby="demo-row-radio-buttons-group-label"
                          name="row-radio-buttons-group"
                          className='mb-4'
                          value={gender}
                          defaultValue={gender}
                          onChange={(e) => setGender(e.target.value)}
                        >
                          <FormControlLabel value="female" control={<Radio />} label="Female" />
                          <FormControlLabel value="male" control={<Radio />} label="Male" />
                          <FormControlLabel value="other" control={<Radio />} label="Other" />
                        </RadioGroup>
                        <MDBRow>
                          <MDBCol md='6'>
                            <Autocomplete
                              id="country"
                              //sx={{ width: 300 }}
                              options={countries}
                              defaultValue={{ code: 'CN', label: 'China', phone: '86' }}
                              autoHighlight
                              getOptionLabel={(option) => option.label}
                              renderOption={(props, option) => (
                                <Box component="li" sx={{ '& > img': { mr: 2, flexShrink: 0 } }} {...props}>
                                  <img
                                    loading="lazy"
                                    width="20"
                                    src={`https://flagcdn.com/w20/${option.code.toLowerCase()}.png`}
                                    srcSet={`https://flagcdn.com/w40/${option.code.toLowerCase()}.png 2x`}
                                    alt=""
                                  />
                                  {option.label} ({option.code}) +{option.phone}
                                </Box>
                              )}
                              renderInput={(params) => (
                                <TextField
                                  {...params}
                                  label="Choose a country"
                                  onChange={(e) => setCountry(e.target.value)}
                                  inputProps={{
                                    ...params.inputProps,
                                    autoComplete: 'new-password', // disable autocomplete and autofill
                                  }}
                                />
                              )}
                            />
                          </MDBCol>
                          <MDBCol md='6'>
                            <Autocomplete
                              id="ort"
                              //sx={{ width: 200 }}
                              options={china_provinces}
                              value={ort}
                              onChange={(event, value) => setOrt(value)}
                              autoHighlight
                              renderInput={(params) => (
                                <TextField
                                  {...params}
                                  label="Choose a ort"
                                  // onChange={(e) => setOrt(e.target.value)}
                                  inputProps={{
                                    ...params.inputProps,
                                    autoComplete: 'new-password', // disable autocomplete and autofill
                                  }}
                                />
                              )}
                            />
                          </MDBCol>
                        </MDBRow>
                        <TextField id="email" label="Email" size="lg" variant="outlined" value={email}
                          onChange={(e) => setEmail(e.target.value)} type='email' inputProps={{ readOnly: true }} className='my-4' />
                        <TextField id="phone" label="Phone" variant="outlined" value={phone}
                          onChange={(e) => setPhone(e.target.value)} type='text' className='mb-4' />
                        <TextField id="password" label="Password" variant="outlined" value={password} inputProps={{ required: true }}
                          onChange={(e) => setPassword(e.target.value)} type='password' className='mb-4' />
                        <div className="d-flex justify-content-end pt-3">
                          <Stack direction="row" spacing={2}>
                            <Button variant="outlined" startIcon={<RefreshIcon />}>
                              Reset
                            </Button>
                            <Button variant="contained" type="submit" endIcon={<SendIcon />}>
                              Submit
                            </Button>
                          </Stack>
                        </div>
                      </MDBCardBody>
                    </form>
                  </Box>
                </Box>
              </Grid>
            </Grid>
          </Grid>
        </Box>
        <Rightbar></Rightbar>
      </Stack>
    </Box>

  );
}

const RadioButton = ({ label, value, onChange }) => {
  return (
    <label>
      <input type="radio" checked={value} onChange={onChange} />
      {label}
    </label>
  );
};

export const china_provinces = ["Anhui", "Fujian", "Gansu", "Guangdong", "Guizhou", "Hainan", "Hebei", "Heilongjiang", "Henan", "Hubei", "Hunan", "Jiangsu", "Jiangxi", "Jilin", "Liaoning", "Qinghai", "Shaanxi", "Shandong", "Shanxi", "Sichuan", "Yunnan", "Zhejiang", "Guangxi", "Nei Mongol", "Ningxia", "Xinjiang", "Xizang (Tibet)", "Beijing", "Chongqing", "Shanghai", "Tianjin"]

// From https://bitbucket.org/atlassian/atlaskit-mk-2/raw/4ad0e56649c3e6c973e226b7efaeb28cb240ccb0/packages/core/select/src/data/countries.js
export const countries = ['China'
  //{ code: 'CN', label: 'China', phone: '86' },
];

export default Register;