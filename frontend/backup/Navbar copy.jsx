//import { Search, ShoppingCartOutlined } from "@material-ui/icons";
import React from "react";
import styled from "styled-components";
import { mobile } from "../responsive";
import { Link } from "react-router-dom";
import { green } from "@material-ui/core/colors";
import { useNavigate } from "react-router";
import Button from '@mui/material/Button';
import Badge from '@mui/material/Badge';
import IconButton from '@mui/material/IconButton';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import Search from '@mui/icons-material/Search';
import Person from '@mui/icons-material/Person';
import Box from '@mui/material/Box';
import { fetchAccessToken, setAccessToken, fetchRefreshToken, setRefreshToken, setUserName, fetchUserName} from "../auth";


const Container = styled.div`
  height: 60px;
  padding: 10px 50px;
  ${mobile({ height: "50px" })}
`;

const Wrapper = styled.div`
  padding: 10px 50px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  ${mobile({ padding: "10px 0px" })}
`;

const Left = styled.div`
  flex: 1;
  display: flex;
  align-items: center;
`;

const Language = styled.span`
  font-size: 14px;
  cursor: pointer;
  ${mobile({ display: "none" })}
`;

const SearchContainer = styled.div`
  border: 0.5px solid lightgray;
  display: flex;
  align-items: center;
  margin-left: 25px;
  padding: 5px;
`;

const Input = styled.input`
  border: none;
  ${mobile({ width: "50px" })}
`;

const Center = styled.div`
  flex: 1;
  text-align: center;
`;

const Logo = styled.h1`
  font-weight: bold;
  ${mobile({ fontSize: "24px" })}
`;
const Right = styled.div`
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  ${mobile({ flex: 2, justifyContent: "center" })}
`;

const MenuItem = styled.div`
  font-size: 14px;
  cursor: pointer;
  margin-left: 25px;
  ${mobile({ fontSize: "12px", marginLeft: "10px" })}
`;

const Navbar = () => {
  const navigate = useNavigate();
  const signOut = () => {
    localStorage.removeItem("UserName");
    localStorage.removeItem("UserAccessToken");
    localStorage.removeItem("UserRefreshToken");
    navigate("/");
  };

  return (
    <Container>
      <Wrapper>
        <Left>
          <Logo><img src={process.env.PUBLIC_URL + '/Logo.png'} style={{ height: 53, width: 53 }} alt="website logo"/></Logo>
          <Button href="/ProductList">Service</Button>
          <Button href="/employee">Members</Button>
          <Button href="/community">Community</Button>
          <Button href="/aboutus">About us</Button>
        </Left>
        <Center>

        </Center>
        <Right>
        <Language>EN</Language>
        {fetchUserName() 
          ? <Button href="/Profile">{fetchUserName()} </Button>
          : <Button href="/Login">Log In</Button>
        }
          <Box mx={2} sx={{ color: 'action.active' }}>
            <Badge color="secondary" variant="dot">
              <ShoppingCartIcon />
            </Badge>
          </Box>
          <Box mx={2} sx={{ color: 'action.active' }}>
            <Badge color="secondary">
              <Search />
            </Badge>
          </Box>
          <Box mx={2} sx={{ color: 'action.active' }}>
            <Badge color="secondary">
              <Person />
            </Badge>
          </Box>
          
          {fetchUserName() 
          ? <Button variant="contained" onClick={signOut} >
            LOG OUT
            </Button>
          : <Button variant="contained" href="/Register">
            SIGN UP
          </Button>
          }
        </Right>
      </Wrapper>
    </Container>
  );
};

<Container>
      <Wrapper>
        <Left>
          <Logo><Link to={'/'}><img src={process.env.PUBLIC_URL + '/Logo.png'} style={{ height: 53, width: 53 }} alt="website logo" /></Link></Logo>
          <Button href="/ProductList" style={{ color: 'black' }}> Service</Button>
          <Button href="/employee" style={{ color: 'black' }}>Members</Button>
          <Button href="/community" style={{ color: 'black' }}>Community</Button>
          <Button href="/aboutus" style={{ color: 'black' }}>AboutUs</Button>
        </Left>
        <Center>

        </Center>
        <Right>
          <Input
            id="input-with-icon-adornment"
            startAdornment={
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            }
          />

          <Box mx={2} sx={{ color: 'action.active' }}>
          {fetchUserName() 
          ? 
            <Button variant="contained" onClick={signOut} style={{ "background-color": "#D2EBCD"}} className="text-dark">
            LOG OUT
            </Button>
          : <Link to={'/Login'} style={{ color: 'black' }}>
            <Badge color="secondary">
              <Person />
            </Badge>
          </Link>
          }
          </Box>
        </Right>
      </Wrapper>
    </Container>
export default Navbar;