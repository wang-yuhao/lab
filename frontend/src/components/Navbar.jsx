import { Mail, Notifications, Pets, Person } from "@mui/icons-material";
import {
  AppBar,
  Avatar,
  Badge,
  Box,
  InputBase,
  Menu,
  Button,
  MenuItem,
  styled,
  Toolbar,
  Typography,
} from "@mui/material";
import { Link } from 'react-router-dom';
import  React, { useState } from "react";
import { useNavigate } from "react-router";
import { fetchAccessToken, setAccessToken, fetchRefreshToken, setRefreshToken, setUserName, fetchUserName} from "../auth";

const StyledToolbar = styled(Toolbar)({
  display: "flex",
  justifyContent: "space-between",
});

const Search = styled("div")(({ theme }) => ({
  backgroundColor: "white",
  padding: "0 10px",
  borderRadius: theme.shape.borderRadius,
  width: "40%",
}));

const Icons = styled(Box)(({ theme }) => ({
  display: "none",
  alignItems: "center",
  gap: "20px",
  [theme.breakpoints.up("sm")]: {
    display: "flex",
  },
}));

const UserBox = styled(Box)(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  gap: "10px",
  [theme.breakpoints.up("sm")]: {
    display: "none",
  },
}));
const Navbar = () => {
  const navigate = useNavigate();
  const signOut = () => {
    localStorage.removeItem("UserName");
    localStorage.removeItem("UserAccessToken");
    localStorage.removeItem("UserRefreshToken");
    navigate("/");
  };
  const [open, setOpen] = useState(false);
  return (
    <AppBar position="sticky">
      <StyledToolbar>
        <Typography variant="h6" sx={{ display: { xs: "none", sm: "block" } }}>
        <Link to={'/'}><img src={process.env.PUBLIC_URL + '/Logo.png'} style={{ height: 53, width: 53 }} alt="website logo" /></Link>
        <Button href="/ProductList" style={{ color: 'black' }}> Service</Button>
        <Button href="/employee" style={{ color: 'black' }}>Members</Button>
        <Button href="/community" style={{ color: 'black' }}>Community</Button>
        <Button href="/aboutus" style={{ color: 'black' }}>AboutUs</Button>
        </Typography>
        <Pets sx={{ display: { xs: "block", sm: "none" } }} />
        
        <Search>
          <InputBase placeholder="search..." />
        </Search>
        <Icons>
          <Badge badgeContent={4} color="error">
            <Mail />
          </Badge>
          <Badge badgeContent={2} color="error">
            <Notifications />
          </Badge>
          {fetchUserName() 
          ? 
          <Avatar
            sx={{ width: 30, height: 30 }}
            src="https://images.pexels.com/photos/846741/pexels-photo-846741.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
            onClick={(e) => setOpen(true)}
          />
          :
          <Person             
            sx={{ width: 30, height: 30 }}
            onClick={(e) => setOpen(true)}
          />
          }
        </Icons>
        {fetchUserName() 
        ? 
        <UserBox onClick={(e) => setOpen(true)}>
          <Avatar
            sx={{ width: 30, height: 30 }}
            src="https://images.pexels.com/photos/846741/pexels-photo-846741.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
          />
          <Typography variant="span">fetchUserName()</Typography>
        </UserBox>
        :
        <UserBox onClick={(e) => setOpen(true)}>
          <Person />
        </UserBox>
        }
      </StyledToolbar>
      {fetchUserName() 
        ? 
        <Menu
          id="demo-positioned-menu"
          aria-labelledby="demo-positioned-button"
          open={open}
          onClose={(e) => setOpen(false)}
          anchorOrigin={{
            vertical: "top",
            horizontal: "right",
          }}
          transformOrigin={{
            vertical: "top",
            horizontal: "right",
          }}
        >
            <MenuItem component={Link} to="/Profile">Profile</MenuItem>
            <MenuItem onClick={signOut}>Logout</MenuItem>
        </Menu>
        :      
        <Menu
          id="demo-positioned-menu"
          aria-labelledby="demo-positioned-button"
          open={open}
          onClose={(e) => setOpen(false)}
          anchorOrigin={{
            vertical: "top",
            horizontal: "right",
          }}
          transformOrigin={{
            vertical: "top",
            horizontal: "right",
          }}
        >
            <MenuItem component={Link} to="/Login">Log In</MenuItem>
            <MenuItem component={Link} to="/Register">Sign Up</MenuItem>
        </Menu>
      }
    </AppBar>
  );
};

export default Navbar;