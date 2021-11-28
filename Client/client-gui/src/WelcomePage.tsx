import blockchain from "./blockchain.svg";
import "./WelcomePage.css";
import LoadingButton from "@mui/lab/LoadingButton";
import ConnectWithoutContactIcon from "@mui/icons-material/ConnectWithoutContact";
import { Typography } from "@mui/material";
import { useState } from "react";
import { SnackbarProvider, useSnackbar, VariantType } from "notistack";
import { useNavigate } from "react-router";
import TextField from "@mui/material/TextField";
import { withStyles } from "@material-ui/core/styles";
import PersonIcon from "@mui/icons-material/Person";

const styles = {
  input: {
    color: "white",
  },
};

function PageBody(props: { classes: any }) {
  const { enqueueSnackbar } = useSnackbar();
  const [registerLoading, setRegisterLoading] = useState(false);
  const [loginLoading, setLoginLoading] = useState(false);
  const navigate = useNavigate();
  const [enteredName, setEnteredName] = useState("");
  const [registeredClientName, setRegisteredClientName] = useState("");
  const [serverIpAddress, setServerIpAddress] = useState("");
  const { classes } = props;

  const onRegister = () => {
    setRegisterLoading(true);

    if (
      !/^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/gi.test(
        serverIpAddress
      )
    ) {
      enqueueSnackbar(`Failed to register: Invalid IP Address!`, {
        variant: "error" as VariantType,
      });
      setRegisterLoading(false);
    } else {
      fetch("/register", {
        method: "POST",
        body: JSON.stringify({
          name: enteredName,
          serverIpAddress: serverIpAddress,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.register === true) {
            navigate(`app`);
          } else {
            enqueueSnackbar(`Failed to register: ${data.register}`, {
              variant: "error" as VariantType,
            });
            setRegisterLoading(false);
          }
        });
    }
  };

  const onLogin = () => {
    setLoginLoading(true);

    fetch("/login", {
      method: "POST",
      body: JSON.stringify({
        name: registeredClientName,
        serverIpAddress: serverIpAddress,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.login === true) {
          navigate(`app`);
        } else {
          enqueueSnackbar(`User does not exist. Please Register instead.`, {
            variant: "error" as VariantType,
          });
          setLoginLoading(false);
        }
      });
  };

  return (
    <>
      <div className="App">
        <header className="App-header">
          <div style={{ paddingTop: "150px" }}>
            <img src={blockchain} className="App-logo" alt="logo" />
          </div>
          <p className="App-title">
            Welcome to P2PFS, a Peer to Peer File Sharing system.
          </p>

          <p className="Textfield-title">Register as a New Client</p>
          <div>
            <TextField
              style={{ width: 300 }}
              InputProps={{
                style: { color: "white", fontSize: "20px" },
                className: classes.input,
              }}
              InputLabelProps={{
                style: { color: "white", fontSize: "20px" },
                className: classes.input,
              }}
              id="client-name"
              label="Name"
              variant="standard"
              color="primary"
              onChange={(event) => setEnteredName(event.target.value)}
            />
          </div>
          <div>
            <TextField
              style={{ width: 300 }}
              InputProps={{
                style: { color: "white", fontSize: "20px" },
                className: classes.input,
              }}
              InputLabelProps={{
                style: { color: "white", fontSize: "20px" },
                className: classes.input,
              }}
              id="client-name"
              label="Server IP Address"
              variant="standard"
              color="primary"
              onChange={(event) => setServerIpAddress(event.target.value)}
            />
          </div>
          <div className="Register-button">
            <LoadingButton
              variant="contained"
              size="large"
              style={{ width: 300, height: 60, borderRadius: 50 }}
              endIcon={<ConnectWithoutContactIcon />}
              onClick={onRegister}
              loading={registerLoading}
              loadingPosition="end"
            >
              <Typography>Register</Typography>
            </LoadingButton>
          </div>

          <p className="Textfield-title">Login to an Existing Client</p>
          <div>
            <TextField
              style={{ width: 300 }}
              InputProps={{
                style: { color: "white", fontSize: "20px" },
                className: classes.input,
              }}
              InputLabelProps={{
                style: { color: "white", fontSize: "20px" },
                className: classes.input,
              }}
              id="client-name"
              label="Registered Client Name"
              variant="standard"
              color="primary"
              onChange={(event) => setRegisteredClientName(event.target.value)}
            />
          </div>
          <div>
            <TextField
              style={{ width: 300 }}
              InputProps={{
                style: { color: "white", fontSize: "20px" },
                className: classes.input,
              }}
              InputLabelProps={{
                style: { color: "white", fontSize: "20px" },
                className: classes.input,
              }}
              id="client-name"
              label="Server IP Address"
              variant="standard"
              color="primary"
              onChange={(event) => setServerIpAddress(event.target.value)}
            />
          </div>
          <div className="Register-button" style={{ paddingBottom: 100 }}>
            <LoadingButton
              variant="contained"
              size="large"
              style={{ width: 300, height: 60, borderRadius: 50 }}
              endIcon={<PersonIcon />}
              onClick={onLogin}
              loading={loginLoading}
              loadingPosition="end"
            >
              <Typography>Log in</Typography>
            </LoadingButton>
          </div>
        </header>
      </div>
    </>
  );
}

function WelcomePage(props: JSX.IntrinsicAttributes & { classes: any }) {
  return (
    <SnackbarProvider maxSnack={3}>
      <PageBody {...props} />
    </SnackbarProvider>
  );
}

export default withStyles(styles)(WelcomePage);
