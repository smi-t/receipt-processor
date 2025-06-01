import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import ReceiptIcon from '@mui/icons-material/Receipt';

function Navbar() {
  return (
    <AppBar position="static">
      <Toolbar>
        <ReceiptIcon sx={{ mr: 2 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Receipt Processor
        </Typography>
        <Button
          color="inherit"
          component={RouterLink}
          to="/"
        >
          Receipts
        </Button>
        <Button
          color="inherit"
          component={RouterLink}
          to="/upload"
        >
          Upload
        </Button>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar; 