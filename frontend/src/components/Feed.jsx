import React, { useState, useEffect } from 'react';
import { styled, useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import MuiDrawer from '@mui/material/Drawer';
import MuiAppBar from '@mui/material/AppBar';
import CssBaseline from '@mui/material/CssBaseline';
import { fetchAccessToken, setAccessToken, fetchRefreshToken, setRefreshToken, setUserName, fetchUserName, setUserRole } from "../auth";
import { china_provinces, countries } from "../pages/Register";

import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Unstable_Grid2'; // Grid version 2
import Stack from '@mui/material/Stack';
import axios from "axios";
import {
    MDBCardBody,
    MDBRow,
    MDBCol,
}
    from 'mdb-react-ui-kit';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import dayjs, { Dayjs } from 'dayjs';
import TextField from '@mui/material/TextField';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import Autocomplete from '@mui/material/Autocomplete';
import Button from '@mui/material/Button';
import RefreshIcon from '@mui/icons-material/Refresh';
import SendIcon from '@mui/icons-material/Send';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import { useNavigate } from "react-router";
import { mobile } from "../responsive";

const drawerWidth = 240;

const openedMixin = (theme) => ({
    width: drawerWidth,
    transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
    }),
    overflowX: 'hidden',
});

const closedMixin = (theme) => ({
    transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
    overflowX: 'hidden',
    width: `calc(${theme.spacing(7)} + 1px)`,
    [theme.breakpoints.up('sm')]: {
        width: `calc(${theme.spacing(8)} + 1px)`,
    },
});

const DrawerHeader = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
}));

const AppBar = styled(MuiAppBar, {
    shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
    ...(open && {
        marginLeft: drawerWidth,
        width: `calc(100% - ${drawerWidth}px)`,
        transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
    }),
}));

const Item = styled(Paper)(({ theme }) => ({
    backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
    ...theme.typography.body2,
    padding: theme.spacing(1),
    textAlign: 'center',
    color: theme.palette.text.secondary,
}));

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
    ({ theme, open }) => ({
        width: drawerWidth,
        flexShrink: 0,
        whiteSpace: 'nowrap',
        boxSizing: 'border-box',
        ...(open && {
            ...openedMixin(theme),
            '& .MuiDrawer-paper': openedMixin(theme),
        }),
        ...(!open && {
            ...closedMixin(theme),
            '& .MuiDrawer-paper': closedMixin(theme),
        }),
    }),
);



export const Feed = () => {
    const navigate = useNavigate();
    const theme = useTheme();
    const [open, setOpen] = React.useState(false);
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [phone, setPhone] = useState("");
    const [gender, setGender] = useState("");
    const [message, setMessage] = useState("");
    const [birthdate, setBirthdate] = useState("");
    const [password, setPassword] = useState("");
    const [country, setCountry] = useState("");
    const [ort, setOrt] = useState("");
    const [role, setRole] = useState("");
    const refresh_token = fetchRefreshToken();

    let handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // make api call to our backend. we'll leave thisfor later
            axios.post("http://0.0.0.0:8000/user/update_user", {
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
                    'Authorization': 'Bearer ' + fetchRefreshToken()
                }
            }).then(function (response, request) {
                console.log(response.data.access_token, "response.data.access_token");
                console.log(response.data.refresh_token, "response.data.refresh_token");
                if (response.data.access_token) {
                    setAccessToken(response.data.access_token);
                    setRefreshToken(response.data.refresh_token);
                    setUserName(name);
                    navigate("/");
                }
            })
                .catch(function (error) {
                    console.log(error, "error");
                });

        } catch (err) {
            console.log(err);
        }
    };


    const handleDrawerOpen = () => {
        setOpen(true);
    };

    const handleDrawerClose = () => {
        setOpen(false);
    };

    useEffect(() => {
        // make api call to our backend. we'll leave thisfor later
        axios.get("http://0.0.0.0:8000/user/profile", {
            headers: {
                'accept': 'application/json',
                'Authorization': 'Bearer ' + fetchRefreshToken()
            }
        }).then(function (response) {
            console.log(response.data.email, "response.data.email");
            if (response.data) {
                setName(response.data.name);
                setEmail(response.data.email);
                setBirthdate(response.data.birth_date);
                setUserName(response.data.name);
                setCountry(response.data.country);
                setOrt(response.data.ort);
                setGender(response.data.gender);
                setPhone(response.data.phone_number);
                setUserRole(response.data.role);
                setRole(response.data.role);
            }
        })
    }, []);

    return (
        <Box flex={4} p={2}>
            <Grid sx={{flexGrow: 1}} container spacing={2} justifyContent="center" alignItems="center">
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
                                        <h3 className="mb-5 text-uppercase fw-bold">Profile</h3>
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
                                                    value={countries}
                                                    onChange={(event, value) => setCountry(value)}
                                                    //defaultValue={{ code: 'CN', label: 'China', phone: '86' }}
                                                    autoHighlight
                                                    //getOptionLabel={(option) => option.label}
                                                    renderInput={(params) => (
                                                        <TextField
                                                            {...params}
                                                            label="Choose a country"
                                                            // onChange={(e) => setOrt(e.target.value)}
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
                                        <TextField id="password" label="Password" variant="outlined" value={password}
                                            onChange={(e) => setPassword(e.target.value)} type='password' className='mb-4' />
                                        <div className="d-flex justify-content-end pt-3">
                                            <Stack direction="row" spacing={2}>
                                                <Button variant="outlined" startIcon={<RefreshIcon />}>
                                                    Reset
                                                </Button>
                                                <Button variant="contained" type="submit" endIcon={<SendIcon />}>
                                                    Save
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
    )
}
