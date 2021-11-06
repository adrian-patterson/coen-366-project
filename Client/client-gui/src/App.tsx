import blockchain from './blockchain.svg';
import './WelcomePage.css';
import LoadingButton from '@mui/lab/LoadingButton';
import ConnectWithoutContactIcon from '@mui/icons-material/ConnectWithoutContact';
import { Typography } from '@mui/material';
import { useEffect, useState } from 'react';
import { SnackbarProvider, VariantType, useSnackbar } from 'notistack';
import React from 'react';
import { useParams } from 'react-router';


 function PageBody() {
  const { enqueueSnackbar } = useSnackbar();
  const { name } = useParams();

  useEffect(() => {
    enqueueSnackbar("Registration Successful!", { variant: 'success' as VariantType});

      return () => {
        fetch('/de_register', { method: 'POST', body: JSON.stringify({ name: name}) });
        }
  }, []);

  return(
  <>
    <div className="App">
      <header className="App-header">
        <p className="App-title">
          Time to get transferring.
        </p>
      </header>
    </div>
  </>);
}

export default function App() {
  return(
    <SnackbarProvider maxSnack={3}>
      <PageBody />
    </SnackbarProvider>
  );
}
