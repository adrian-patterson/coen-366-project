import { useEffect, useState } from "react";
import { SnackbarProvider, VariantType, useSnackbar } from "notistack";
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
import PersonIcon from "@mui/icons-material/Person";
import Collapse from "@mui/material/Collapse";
import { ExpandLess, ExpandMore } from "@mui/icons-material";
import UpdateIcon from "@mui/icons-material/Update";
import DownloadIcon from "@mui/icons-material/Download";

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

export type Client = {
  name: string;
  ipAddress: string;
  udpSocket: string;
  tcpSocket: string;
  listOfAvailableFiles: string[];
};

function PageBody(props: { classes: any }) {
  const { enqueueSnackbar } = useSnackbar();
  const [client, setClient] = useState<Client>();
  const [clientFiles, setClientFiles] = useState<string[]>([]);
  const [clientIpAddress, setClientIpAddress] = useState("");
  const [clientUdpSocket, setClientUdpSocket] = useState("");
  const [clientTcpSocket, setClientTcpSocket] = useState("");
  const [filesSelected, setFilesSelected] = useState<number[]>([]);
  const [clientsExpanded, setClientsExpanded] = useState<string[]>([]);
  const [clientsDiscovered, setClientsDiscovered] = useState<Client[]>([]);
  const [filesDiscovered, setFilesDiscovered] = useState<string[]>([]);
  const [searchedClient, setSearchedClient] = useState("");
  const [searchedFile, setSearchedFile] = useState("");
  const { classes } = props;

  useEffect(() => {
    enqueueSnackbar("Registration Successful!", {
      variant: "success" as VariantType,
    });

    fetch("/client")
      .then((response) => {
        return response.json();
      })
      .then((client: Client) => {
        setClient(client);
        setClientFiles(client.listOfAvailableFiles);
      });

    const exClient: Client = {
      name: "Me",
      ipAddress: "4352345",
      listOfAvailableFiles: ["MYYY FILE 1", "MY FILE @", "ETC BB"],
      udpSocket: "324234",
      tcpSocket: "324234",
    };
    setClient(exClient);
    setClientFiles(exClient.listOfAvailableFiles);

    return () => {
      fetch("/de_register", {
        method: "POST",
      });
    };
  }, []);

  const onUpdateUserInfo = () => {
    console.log(
      `IP Address: ${clientIpAddress}\nUDP Socket: ${clientUdpSocket}\nTCP Socket: ${clientTcpSocket}`
    );
  };

  const onPublishFiles = () => {
    let fileList: string[] = [];
    filesSelected.forEach((fileIndex) => {
      fileList.push(client?.listOfAvailableFiles[fileIndex] ?? "");
    });
    fetch("/publish", {
      method: "POST",
      body: JSON.stringify({
        filesSelected: fileList,
      }),
    });
  };

  const onRemoveFiles = () => {
    let fileList: string[] = [];
    filesSelected.forEach((fileIndex) => {
      fileList.push(client?.listOfAvailableFiles[fileIndex] ?? "");
    });
    fetch("/remove", {
      method: "POST",
      body: JSON.stringify({
        filesSelected: fileList,
      }),
    });
  };

  const onSearchAllClients = () => {
    console.log("Search all clients clicked");
    const clients: Client[] = [
      {
        name: "Adrian",
        ipAddress: "127.0.0.1",
        udpSocket: "8080",
        tcpSocket: "800",
        listOfAvailableFiles: ["Legend of Zelda", "Thingy"],
      },
      {
        name: "Ya boi",
        ipAddress: "127.0.0.1",
        udpSocket: "8080",
        tcpSocket: "80000",
        listOfAvailableFiles: ["Legend of Jawn", "Jawny"],
      },
    ];
    setClientsDiscovered(clients);
    let files: string[] = [];
    clients.forEach((client) => {
      client.listOfAvailableFiles.forEach((file) => {
        files.push(file);
      });
    });
    setFilesDiscovered(files);
  };

  const onSearchAllFiles = () => {
    console.log("Search all files clicked");
  };

  const onSearchClient = () => {
    console.log("Client searched: " + searchedClient);
  };

  const onSearchFile = () => {
    console.log("File searched: " + searchedFile);
    const searchedFileResult = searchedFile;
    const sampleresultFile: string = "Result File search!";
    setFilesDiscovered([sampleresultFile]);
    //setFile;
  };

  const handleToggleFiles = (value: number) => () => {
    const currentIndex = filesSelected.indexOf(value);
    const newChecked = [...filesSelected];

    if (currentIndex === -1) {
      newChecked.push(value);
    } else {
      newChecked.splice(currentIndex, 1);
    }

    setFilesSelected(newChecked);
  };

  const handleExpandClient = (clientName: string) => {
    const currentIndex = clientsExpanded.indexOf(clientName);
    const newExpanded = [...clientsExpanded];

    if (currentIndex === -1) {
      newExpanded.push(clientName);
    } else {
      newExpanded.splice(currentIndex, 1);
    }
    setClientsExpanded(newExpanded);
  };

  // let clients: Client[] = [
  //   {
  //     rq: 0,
  //     name: "Adrian",
  //     ipAddress: "127.0.0.1",
  //     udpSocket: "8080",
  //     tcpSocket: "800",
  //     listOfAvailableFiles: ["Legend of Zelda", "Thingy"],
  //   },
  //   {
  //     rq: 1,
  //     name: "Ya boi",
  //     ipAddress: "127.0.0.1",
  //     udpSocket: "8080",
  //     tcpSocket: "80000",
  //     listOfAvailableFiles: ["Legend of Jawn", "Jawny"],
  //   },
  // ];

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
                <p className="Grid-titles">{client ? client.name : ""}</p>

                <Box sx={{ width: "100%" }}>
                  <Grid
                    container
                    rowSpacing={1}
                    columnSpacing={{ xs: 1, sm: 2, md: 3 }}
                  >
                    <Grid
                      item
                      xs={6}
                      style={{ paddingBottom: "20px", paddingLeft: "50px" }}
                      display="flex"
                      justifyContent="flex-start"
                    >
                      <p className="Grid-titles">
                        <b>IP Address:</b> {client?.ipAddress}
                      </p>
                    </Grid>
                    <Grid
                      item
                      xs={6}
                      style={{ paddingBottom: "20px", paddingLeft: "30px" }}
                      display="flex"
                      justifyContent="flex-start"
                    >
                      <TextField
                        style={{ width: 330 }}
                        InputProps={{
                          style: { color: "white", fontSize: "20px" },
                          className: classes.input,
                        }}
                        InputLabelProps={{
                          style: { color: "white", fontSize: "16px" },
                          className: classes.input,
                        }}
                        id="client-search"
                        label="Enter a new IP Address"
                        variant="standard"
                        color="primary"
                        onChange={(event) =>
                          setClientIpAddress(event.target.value)
                        }
                      />
                    </Grid>
                  </Grid>
                  <Grid
                    container
                    rowSpacing={1}
                    columnSpacing={{ xs: 1, sm: 2, md: 3 }}
                  >
                    <Grid
                      item
                      xs={6}
                      style={{ paddingBottom: "20px", paddingLeft: "50px" }}
                      display="flex"
                      justifyContent="flex-start"
                    >
                      <p className="Grid-titles">
                        <b>UDP Socket:</b> {client?.udpSocket}
                      </p>
                    </Grid>
                    <Grid
                      item
                      xs={6}
                      style={{ paddingBottom: "20px", paddingLeft: "30px" }}
                      display="flex"
                      justifyContent="flex-start"
                    >
                      <TextField
                        style={{ width: 330 }}
                        InputProps={{
                          style: { color: "white", fontSize: "20px" },
                          className: classes.input,
                        }}
                        InputLabelProps={{
                          style: { color: "white", fontSize: "16px" },
                          className: classes.input,
                        }}
                        id="client-search"
                        label="Enter a new UDP Socket"
                        variant="standard"
                        color="primary"
                        onChange={(event) =>
                          setClientUdpSocket(event.target.value)
                        }
                      />
                    </Grid>
                    <Grid
                      container
                      rowSpacing={1}
                      columnSpacing={{ xs: 1, sm: 2, md: 3 }}
                      style={{ paddingLeft: "20px" }}
                    >
                      <Grid
                        item
                        xs={6}
                        style={{ paddingBottom: "20px", paddingLeft: "50px" }}
                        display="flex"
                        justifyContent="flex-start"
                      >
                        <p className="Grid-titles">
                          <b>TCP Socket:</b> {client?.tcpSocket}
                        </p>
                      </Grid>
                      <Grid
                        item
                        xs={6}
                        style={{ paddingBottom: "20px", paddingLeft: "30px" }}
                        display="flex"
                        justifyContent="flex-start"
                      >
                        <TextField
                          style={{ width: 330 }}
                          InputProps={{
                            style: { color: "white", fontSize: "20px" },
                            className: classes.input,
                          }}
                          InputLabelProps={{
                            style: { color: "white", fontSize: "16px" },
                            className: classes.input,
                          }}
                          id="client-search"
                          label="Enter a new TCP Socket"
                          variant="standard"
                          color="primary"
                          onChange={(event) =>
                            setClientTcpSocket(event.target.value)
                          }
                        />
                      </Grid>
                    </Grid>
                  </Grid>
                  <Grid
                    container
                    rowSpacing={1}
                    columnSpacing={{ xs: 1, sm: 2, md: 3 }}
                  >
                    <Grid
                      item
                      xs={6}
                      style={{ paddingBottom: "20px", paddingLeft: "30px" }}
                      display="flex"
                      justifyContent="flex-start"
                    ></Grid>
                    <Grid
                      item
                      xs={6}
                      style={{ paddingBottom: "20px", paddingLeft: "100px" }}
                      display="flex"
                      justifyContent="flex-start"
                    >
                      <LoadingButton
                        variant="contained"
                        size="large"
                        style={{ width: 200, height: 60, borderRadius: 5 }}
                        endIcon={<UpdateIcon />}
                        onClick={onUpdateUserInfo}
                        // loading={registerLoading}
                        loadingPosition="end"
                      >
                        Update
                      </LoadingButton>
                    </Grid>
                  </Grid>
                </Box>
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
                  {clientFiles.map((file, index) => {
                    const labelId = `checkbox-list-label-${file}`;

                    return (
                      <ListItem
                        key={file}
                        secondaryAction={
                          <Icon>
                            <DescriptionIcon style={{ color: "white" }} />
                          </Icon>
                        }
                        disablePadding
                      >
                        <ListItemButton
                          role={undefined}
                          onClick={handleToggleFiles(index)}
                          dense
                        >
                          <ListItemIcon>
                            <Checkbox
                              edge="start"
                              style={{ color: "white" }}
                              checked={filesSelected.indexOf(index) !== -1}
                              tabIndex={-1}
                              disableRipple
                              inputProps={{ "aria-labelledby": labelId }}
                            />
                          </ListItemIcon>
                          <ListItemText
                            id={labelId}
                            primary={file}
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
                        onClick={onPublishFiles}
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
                        onClick={onRemoveFiles}
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
                      xs={12}
                      style={{ paddingBottom: "20px", paddingLeft: "30px" }}
                      display="flex"
                      justifyContent="flex-start"
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
                  {clientsDiscovered.map((client) => {
                    return (
                      <Box>
                        <ListItemButton
                          onClick={() => handleExpandClient(client.name)}
                        >
                          <ListItemIcon>
                            <PersonIcon style={{ color: "white" }} />
                          </ListItemIcon>
                          <ListItemText primary={client.name} />
                          {clientsExpanded.indexOf(client.name) !== -1 ? (
                            <ExpandLess />
                          ) : (
                            <ExpandMore />
                          )}
                        </ListItemButton>
                        <Collapse
                          in={clientsExpanded.indexOf(client.name) !== -1}
                          timeout="auto"
                          unmountOnExit
                        >
                          <List component="div" disablePadding>
                            {client.listOfAvailableFiles.map((file) => {
                              return (
                                <ListItemButton sx={{ pl: 4 }}>
                                  <ListItemIcon>
                                    <DescriptionIcon
                                      style={{ color: "white" }}
                                    />
                                  </ListItemIcon>
                                  <ListItemText primary={file} />
                                </ListItemButton>
                              );
                            })}
                          </List>
                        </Collapse>
                      </Box>
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
                        onClick={onSearchAllClients}
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
                      xs={12}
                      style={{ paddingBottom: "20px", paddingLeft: "30px" }}
                      display="flex"
                      justifyContent="flex-start"
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
                  {filesDiscovered.map((file) => {
                    const labelId = `checkbox-list-label-${file}`;

                    return (
                      <ListItem
                        key={file}
                        secondaryAction={
                          <IconButton>
                            <DownloadIcon
                              style={{ color: "white" }}
                              onClick={() => console.log("Download " + file)}
                            />
                          </IconButton>
                        }
                        disablePadding
                      >
                        <ListItemButton role={undefined} dense>
                          <ListItemIcon>
                            <DescriptionIcon
                              style={{ color: "white", paddingBottom: "5px" }}
                            />
                          </ListItemIcon>
                          <ListItemText
                            id={labelId}
                            primary={file}
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
                        onClick={onSearchAllFiles}
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
