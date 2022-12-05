import { Box, Stack } from '@mui/material'
import React from 'react'
import { Feed } from '../components/Feed';
import Rightbar from '../components/Rightbar';
import Sidebar from '../components/Sidebar';


export default function Profile() {
    return (
    <Box>
      <Stack direction="row" spacing={2} justifyContent="space-between">
        <Sidebar></Sidebar>
        <Feed></Feed>
        <Rightbar></Rightbar>
      </Stack>
    </Box>
    
  );
}