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

const styles = {
  input: {
    color: "white",
  },
};

function PageBody(props: { classes: any }) {
  const { enqueueSnackbar } = useSnackbar();
  const [registerLoading, setRegisterLoading] = useState(false);
  const navigate = useNavigate();
  const [enteredName, setEnteredName] = useState("");
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

  return (
    <>
      <div className="App">
        <header className="App-header">
          <img src={blockchain} className="App-logo" alt="logo" />
          <p className="App-title">
            Welcome to P2PFS, a Peer to Peer File Sharing system.
          </p>
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
