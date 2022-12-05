import styled from "styled-components";
import { mobile } from "../responsive";

const Container = styled.div`
  width: 100vw;
  height: 100vh;
  background: linear-gradient(
      rgba(255, 255, 255, 0.5),
      rgba(255, 255, 255, 0.5)
    ),
    url(${process.env.PUBLIC_URL + '/university-of-bonn.jpg'}),

    center;
  background-size: cover;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const Wrapper = styled.div`
  width: 40%;
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
  flex-wrap: wrap;
`;

const Input = styled.input`
  flex: 1;
  min-width: 40%;
  margin: 20px 10px 0px 0px;
  padding: 10px;
`;

const Agreement = styled.span`
  font-size: 12px;
  margin: 20px 0px;
`;

const Button = styled.button`
  width: 40%;
  border: none;
  padding: 15px 20px;
  background-color: teal;
  color: white;
  cursor: pointer;
`;

const Register = () => {
  return (
    <Container>
      <Wrapper>
        <Title>CREATE AN ACCOUNT</Title>
        <Form>
          <Input placeholder="name" />
          <Input placeholder="last name" />
          <Input placeholder="username" />
          <Input placeholder="email" />
          <Input placeholder="password" />
          <Input placeholder="confirm password" />
          <Agreement>
            By creating an account, I consent to the processing of my personal
            data in accordance with the <b>PRIVACY POLICY</b>
          </Agreement>
          <Button>CREATE</Button>
        </Form>
      </Wrapper>
    </Container>
  );
};

export default Register;

<MDBContainer fluid className='bg-dark'>

<MDBRow className='d-flex justify-content-center align-items-center h-100'>
  <MDBCol>

    <MDBCard className='my-4'>
      <MDBRow className='g-0'>
        <MDBCol md='6' className="d-none d-md-block">
          <MDBCardImage src='https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-registration/img4.webp' alt="Sample photo" className="rounded-start" fluid />
        </MDBCol>
        <MDBCol md='6'>
          <form onSubmit={handleSubmit}>

            <MDBCardBody className='text-black d-flex flex-column justify-content-center'>
              <h3 className="mb-5 text-uppercase fw-bold">Student registration form</h3>
              <TextField id="name" label="Name" inputProps={{ required: true }} value={name}
                onChange={(e) => setName(e.target.value)} variant="outlined" className='mb-4' />

              <LocalizationProvider dateAdapter={AdapterDayjs} wrapperClass='mb-4'>
                <DatePicker
                  disableFuture
                  label="Birth date"
                  openTo="year"
                  views={['year', 'month', 'day']}
                  value={birthdate}
                  onChange={(newValue) => {
                    setBirhtdate(newValue);
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
                        value={country}
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
                    autoHighlight
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        label="Choose a ort"
                        value={ort}
                        onChange={(e) => setOrt(e.target.value)}
                        inputProps={{
                          ...params.inputProps,
                          autoComplete: 'new-password', // disable autocomplete and autofill
                        }}
                      />
                    )}
                  />
                </MDBCol>
              </MDBRow>
              <TextField id="email" label="Email" size="lg" variant="outlined" value={email} inputProps={{ required: true }}
                onChange={(e) => setEmail(e.target.value)} type='text' className='my-4' />
              <TextField id="phone" label="Phone" variant="outlined" value={phone}
                onChange={(e) => setPhone(e.target.value)} type='text' className='mb-4' />
              <TextField id="password" label="Password" variant="outlined" value={password} inputProps={{ required: true }}
                onChange={(e) => setPassword(e.target.value)} type='password' className='mb-4' />
              <div className="d-flex justify-content-end pt-3">
                <Stack direction="row" spacing={2}>
                  <Button variant="outlined" startIcon={<RefreshIcon />}>
                    Reset all
                  </Button>
                  <Button variant="contained" type="submit" endIcon={<SendIcon />}>
                    Submit form
                  </Button>
                </Stack>
              </div>

            </MDBCardBody>
          </form>
        </MDBCol>
      </MDBRow>
    </MDBCard>
  </MDBCol>
</MDBRow>
</MDBContainer>