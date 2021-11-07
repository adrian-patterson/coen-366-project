import { useEffect, useState } from "react";
import { SnackbarProvider, VariantType, useSnackbar } from "notistack";
import { useParams } from "react-router";
import "./App.css";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Checkbox from "@mui/material/Checkbox";
import Icon from "@mui/material/Icon";
import DescriptionIcon from "@mui/icons-material/Description";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import { styled } from "@mui/material/styles";
import Paper from "@mui/material/Paper";
import LoadingButton from "@mui/lab/LoadingButton";
import FileUploadIcon from "@mui/icons-material/FileUpload";
import DeleteIcon from "@mui/icons-material/Delete";
import { Typography } from "@mui/material";
import TextField from "@material-ui/core/TextField";
import withStyles from "@material-ui/styles/withStyles";
import IconButton from "@mui/material/IconButton";
import SearchIcon from "@mui/icons-material/Search";

const Item = styled(Paper)(({ theme }) => ({
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: "center",
  color: "white",
  backgroundColor: "#3b414b",
}));

const styles = {
  input: {
    color: "white",
  },
};

function PageBody(props: { classes: any }) {
  const { enqueueSnackbar } = useSnackbar();
  const { name } = useParams();
  const [checked, setChecked] = useState([0]);
  const [searchedClient, setSearchedClient] = useState("");
  const [searchedFile, setSearchedFile] = useState("");
  const { classes } = props;

  useEffect(() => {
    enqueueSnackbar("Registration Successful!", {
      variant: "success" as VariantType,
    });

    return () => {
      fetch("/de_register", {
        method: "POST",
        body: JSON.stringify({ name: name }),
      });
    };
  }, []);

  const onSearchClient = () => {
    console.log("Client searched: " + searchedClient);
  };

  const onSearchFile = () => {
    console.log("File searched: " + searchedFile);
  };

  const handleToggle = (value: number) => () => {
    const currentIndex = checked.indexOf(value);
    const newChecked = [...checked];

    if (currentIndex === -1) {
      newChecked.push(value);
    } else {
      newChecked.splice(currentIndex, 1);
    }

    setChecked(newChecked);
  };

  return (
    <>
      <div className="App">
        <header className="App-page-header">Time to get transferring.</header>

        <Box
          sx={{ width: "100%" }}
          style={{ backgroundColor: "#282c34", paddingBottom: "20px" }}
        >
          <Grid
            container
            rowSpacing={1}
            columnSpacing={{ xs: 1, sm: 2, md: 3 }}
            style={{ paddingLeft: "20px", paddingRight: "20px" }}
          >
            <Grid item xs={12}>
              <Item>
                <p className="Grid-titles">Your Information</p>
              </Item>
            </Grid>

            <Grid item xs={12}>
              <Item>
                <p className="Grid-titles">Your files</p>

                <List
                  sx={{
                    width: "100%",
                    bgcolor: "#282c34",
                    borderRadius: "4px",
                  }}
                >
                  {[0, 1, 2, 3].map((value) => {
                    const labelId = `checkbox-list-label-${value}`;

                    return (
                      <ListItem
                        key={value}
                        secondaryAction={
                          <Icon>
                            <DescriptionIcon style={{ color: "white" }} />
                          </Icon>
                        }
                        disablePadding
                      >
                        <ListItemButton
                          role={undefined}
                          onClick={handleToggle(value)}
                          dense
                        >
                          <ListItemIcon>
                            <Checkbox
                              edge="start"
                              style={{ color: "white" }}
                              checked={checked.indexOf(value) !== -1}
                              tabIndex={-1}
                              disableRipple
                              inputProps={{ "aria-labelledby": labelId }}
                            />
                          </ListItemIcon>
                          <ListItemText
                            id={labelId}
                            primary={`Line item ${value + 1}`}
                            style={{ color: "white" }}
                          />
                        </ListItemButton>
                      </ListItem>
                    );
                  })}
                </List>
                <Box sx={{ width: "100%" }} style={{ paddingTop: "10px" }}>
                  <Grid
                    container
                    rowSpacing={1}
                    columnSpacing={{ xs: 1, sm: 2, md: 3 }}
                  >
                    <Grid item xs={6}>
                      <LoadingButton
                        variant="contained"
                        size="large"
                        style={{ width: 200, height: 60, borderRadius: 5 }}
                        endIcon={<FileUploadIcon />}
                        // onClick={onRegister}
                        // loading={registerLoading}
                        loadingPosition="end"
                      >
                        <Typography>Publish</Typography>
                      </LoadingButton>
                    </Grid>
                    <Grid item xs={6}>
                      <LoadingButton
                        variant="contained"
                        size="large"
                        style={{ width: 200, height: 60, borderRadius: 5 }}
                        endIcon={<DeleteIcon />}
                        // onClick={onRegister}
                        // loading={registerLoading}
                        loadingPosition="end"
                      >
                        <Typography>Remove</Typography>
                      </LoadingButton>
                    </Grid>
                  </Grid>
                </Box>
              </Item>
            </Grid>

            <Grid item xs={12}>
              <Item>
                <p className="Grid-titles">Available Clients</p>
                <Box sx={{ width: "100%" }}>
                  <Grid
                    container
                    rowSpacing={1}
                    columnSpacing={{ xs: 1, sm: 2, md: 3 }}
                  >
                    <Grid
                      item
                      xs={6}
                      style={{ paddingBottom: "20px", paddingLeft: "20px" }}
                    >
                      <TextField
                        style={{ width: 330 }}
                        InputProps={{
                          style: { color: "white", fontSize: "20px" },
                          className: classes.input,
                        }}
                        InputLabelProps={{
                          style: { color: "white", fontSize: "20px" },
                          className: classes.input,
                        }}
                        id="client-search"
                        label="Client Name"
                        variant="standard"
                        color="primary"
                        onChange={(event) =>
                          setSearchedClient(event.target.value)
                        }
                      />
                    </Grid>
                    <Grid
                      item
                      xs={6}
                      style={{ paddingRight: "330px", paddingTop: "25px" }}
                    >
                      <IconButton
                        aria-label="delete"
                        onClick={() => onSearchClient()}
                      >
                        <SearchIcon style={{ color: "white" }} />
                      </IconButton>
                    </Grid>
                  </Grid>
                </Box>
                <List
                  sx={{
                    width: "100%",
                    bgcolor: "#282c34",
                    borderRadius: "4px",
                  }}
                >
                  {[0, 1, 2, 3].map((value) => {
                    const labelId = `checkbox-list-label-${value}`;

                    return (
                      <ListItem
                        key={value}
                        secondaryAction={
                          <Icon>
                            <DescriptionIcon style={{ color: "white" }} />
                          </Icon>
                        }
                        disablePadding
                      >
                        <ListItemButton
                          role={undefined}
                          onClick={handleToggle(value)}
                          dense
                        >
                          <ListItemIcon>
                            <Checkbox
                              edge="start"
                              style={{ color: "white" }}
                              checked={checked.indexOf(value) !== -1}
                              tabIndex={-1}
                              disableRipple
                              inputProps={{ "aria-labelledby": labelId }}
                            />
                          </ListItemIcon>
                          <ListItemText
                            id={labelId}
                            primary={`Line item ${value + 1}`}
                            style={{ color: "white" }}
                          />
                        </ListItemButton>
                      </ListItem>
                    );
                  })}
                </List>
                <Box sx={{ width: "100%" }} style={{ paddingTop: "10px" }}>
                  <Grid
                    container
                    rowSpacing={1}
                    columnSpacing={{ xs: 1, sm: 2, md: 3 }}
                  >
                    <Grid item xs={12}>
                      <LoadingButton
                        variant="contained"
                        size="large"
                        style={{ width: 200, height: 60, borderRadius: 5 }}
                        endIcon={<SearchIcon />}
                        // onClick={onRegister}
                        // loading={registerLoading}
                        loadingPosition="end"
                      >
                        <Typography>Search All</Typography>
                      </LoadingButton>
                    </Grid>
                  </Grid>
                </Box>
              </Item>
            </Grid>

            <Grid item xs={12}>
              <Item>
                <p className="Grid-titles">Available Files</p>
                <Box sx={{ width: "100%" }}>
                  <Grid
                    container
                    rowSpacing={1}
                    columnSpacing={{ xs: 1, sm: 2, md: 3 }}
                  >
                    <Grid
                      item
                      xs={6}
                      style={{ paddingBottom: "20px", paddingLeft: "20px" }}
                    >
                      <TextField
                        style={{ width: 330 }}
                        InputProps={{
                          style: { color: "white", fontSize: "20px" },
                          className: classes.input,
                        }}
                        InputLabelProps={{
                          style: { color: "white", fontSize: "20px" },
                          className: classes.input,
                        }}
                        id="file-search"
                        label="File Name"
                        variant="standard"
                        color="primary"
                        onChange={(event) =>
                          setSearchedFile(event.target.value)
                        }
                      />
                    </Grid>
                    <Grid
                      item
                      xs={6}
                      style={{ paddingRight: "330px", paddingTop: "25px" }}
                    >
                      <IconButton
                        aria-label="delete"
                        onClick={() => onSearchFile()}
                      >
                        <SearchIcon style={{ color: "white" }} />
                      </IconButton>
                    </Grid>
                  </Grid>
                </Box>
                <List
                  sx={{
                    width: "100%",
                    bgcolor: "#282c34",
                    borderRadius: "4px",
                  }}
                >
                  {[0, 1, 2, 3].map((value) => {
                    const labelId = `checkbox-list-label-${value}`;

                    return (
                      <ListItem
                        key={value}
                        secondaryAction={
                          <Icon>
                            <DescriptionIcon style={{ color: "white" }} />
                          </Icon>
                        }
                        disablePadding
                      >
                        <ListItemButton
                          role={undefined}
                          onClick={handleToggle(value)}
                          dense
                        >
                          <ListItemIcon>
                            <Checkbox
                              edge="start"
                              style={{ color: "white" }}
                              checked={checked.indexOf(value) !== -1}
                              tabIndex={-1}
                              disableRipple
                              inputProps={{ "aria-labelledby": labelId }}
                            />
                          </ListItemIcon>
                          <ListItemText
                            id={labelId}
                            primary={`Line item ${value + 1}`}
                            style={{ color: "white" }}
                          />
                        </ListItemButton>
                      </ListItem>
                    );
                  })}
                </List>
                <Box sx={{ width: "100%" }} style={{ paddingTop: "10px" }}>
                  <Grid
                    container
                    rowSpacing={1}
                    columnSpacing={{ xs: 1, sm: 2, md: 3 }}
                  >
                    <Grid item xs={12}>
                      <LoadingButton
                        variant="contained"
                        size="large"
                        style={{ width: 200, height: 60, borderRadius: 5 }}
                        endIcon={<SearchIcon />}
                        // onClick={onRegister}
                        // loading={registerLoading}
                        loadingPosition="end"
                      >
                        <Typography>Search All</Typography>
                      </LoadingButton>
                    </Grid>
                  </Grid>
                </Box>
              </Item>
            </Grid>
          </Grid>
        </Box>
      </div>
    </>
  );
}

function App(props: JSX.IntrinsicAttributes & { classes: any }) {
  return (
    <SnackbarProvider maxSnack={3}>
      <PageBody {...props} />
    </SnackbarProvider>
  );
}

export default withStyles(styles)(App);
