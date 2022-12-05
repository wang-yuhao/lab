import { Box, Stack } from '@mui/material'
import React from 'react'
import { Feed } from '../components/Feed';
import Rightbar from '../components/Rightbar';
import Sidebar from '../components/Sidebar';
import Products from '../components/Products';


export default function Product() {
    return (
    <Box>
      <Stack direction="row" spacing={2} justifyContent="space-between">
        <Sidebar></Sidebar>
        <Products></Products>
        <Rightbar></Rightbar>
      </Stack>
    </Box>
    
  );
}