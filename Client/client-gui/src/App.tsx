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
import { Tooltip, Typography } from "@mui/material";
import { useNavigate } from "react-router";
import TextField from "@material-ui/core/TextField";
import withStyles from "@material-ui/styles/withStyles";
import IconButton from "@mui/material/IconButton";
import SearchIcon from "@mui/icons-material/Search";
import PersonIcon from "@mui/icons-material/Person";
import Collapse from "@mui/material/Collapse";
import { ExpandLess, ExpandMore } from "@mui/icons-material";
import UpdateIcon from "@mui/icons-material/Update";
import DownloadIcon from "@mui/icons-material/Download";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

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
  tcpSocket: string;
  listOfAvailableFiles: string[];
};

export type MyClient = {
  name: string;
  ipAddress: string;
  tcpSocket: string;
  udpSocket: string;
  listOfAvailableFiles: string[];
};

export type File = {
  clientName: string;
  fileName: string;
  ipAddress: string;
  tcpSocket: string;
};

function PageBody(props: { classes: any }) {
  const { enqueueSnackbar } = useSnackbar();
  const [client, setClient] = useState<MyClient>();
  const [clientFiles, setClientFiles] = useState<string[]>([]);
  const [clientIpAddress, setClientIpAddress] = useState("");
  const [clientUdpSocket, setClientUdpSocket] = useState("");
  const [clientTcpSocket, setClientTcpSocket] = useState("");
  const [filesSelected, setFilesSelected] = useState<number[]>([]);
  const [clientsExpanded, setClientsExpanded] = useState<string[]>([]);
  const [clientsDiscovered, setClientsDiscovered] = useState<Client[]>([]);
  const [filesDiscovered, setFilesDiscovered] = useState<File[]>([]);
  const [searchedClient, setSearchedClient] = useState("");
  const [searchedFile, setSearchedFile] = useState("");
  const { classes } = props;
  const navigate = useNavigate();

  useEffect(() => {
    enqueueSnackbar("Registered with Server!", {
      variant: "success" as VariantType,
    });

    fetch("/client")
      .then((response) => {
        return response.json();
      })
      .then((client: MyClient) => {
        setClient(client);
        setClientFiles(client.listOfAvailableFiles);
      });

    return () => {
      fetch("/de_register", {
        method: "POST",
      });
    };
  }, []);

  const onBack = () => {
    fetch("/de_register", {
      method: "POST",
    }).then(() => navigate(`/`));
  };

  const onUpdateUserInfo = () => {
    if (
      !/^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/gi.test(
        clientIpAddress
      )
    ) {
      enqueueSnackbar(`Failed to Update: Invalid IP Address`, {
        variant: "error" as VariantType,
      });
      return;
    } else if (isNaN(Number(clientUdpSocket))) {
      enqueueSnackbar(`Failed to Update: Invalid UDP Socket`, {
        variant: "error" as VariantType,
      });
      return;
    } else if (isNaN(Number(clientTcpSocket))) {
      enqueueSnackbar(`Failed to Update: Invalid TCP Socket`, {
        variant: "error" as VariantType,
      });
      return;
    }

    fetch("/update", {
      method: "POST",
      body: JSON.stringify({
        ipAddress: clientIpAddress,
        udpSocket: clientUdpSocket,
        tcpSocket: clientTcpSocket,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.update === true) {
          enqueueSnackbar(`Successfully updated info!`, {
            variant: "success" as VariantType,
          });
        } else {
          enqueueSnackbar(`Update denied: ${data.update}`, {
            variant: "error" as VariantType,
          });
        }
      });
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
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.publish === true) {
          enqueueSnackbar(`Files published successfully!`, {
            variant: "success" as VariantType,
          });
        } else {
          enqueueSnackbar(`Failed to publish files: ${data.publish}`, {
            variant: "error" as VariantType,
          });
        }
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
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.remove === true) {
          enqueueSnackbar(`Files removed successfully!`, {
            variant: "success" as VariantType,
          });
        } else {
          enqueueSnackbar(`Failed to remove files: ${data.remove}`, {
            variant: "error" as VariantType,
          });
        }
      });
  };

  const onSearchAllClients = () => {
    fetch("/retrieveall")
      .then((response) => response.json())
      .then((retrieve) => {
        const clients = retrieve.retrieve as Client[];
        setClientsDiscovered(clients);

        let files: string[] = [];
        clients.forEach((client) => {
          client.listOfAvailableFiles.forEach((file) => {
            if (!file.includes(file)) {
              files.push(file);
            }
          });
        });
      });
  };

  const onSearchAllFiles = () => {
    fetch("/retrieveall")
      .then(async (response) => {
        if (!response.ok) {
          const result = await response.json();
          enqueueSnackbar(`${searchedClient} not found: ${result.retrieve}`, {
            variant: "error" as VariantType,
          });
          return Promise.reject();
        } else {
          return response.json();
        }
      })
      .then((retrieve) => {
        const clients = retrieve.retrieve as Client[];

        let files: File[] = [];
        clients.forEach((c) => {
          if (c.name !== client?.name)
            c.listOfAvailableFiles.forEach((file) => {
              const f: File = {
                fileName: file,
                clientName: c.name,
                ipAddress: c.ipAddress,
                tcpSocket: c.tcpSocket,
              };
              files.push(f);
            });
        });

        setFilesDiscovered(files);
      });
  };

  const onSearchClient = () => {
    fetch("/retrieve", {
      method: "POST",
      body: JSON.stringify({
        name: searchedClient,
      }),
    })
      .then(async (response) => {
        if (!response.ok) {
          const result = await response.json();
          enqueueSnackbar(`${searchedClient} not found: ${result.retrieve}`, {
            variant: "error" as VariantType,
          });
          return Promise.reject();
        } else {
          return response.json();
        }
      })
      .then((data) => {
        const newClientsList: Client[] = [
          {
            name: data.retrieve.name,
            ipAddress: data.retrieve.ip_address,
            listOfAvailableFiles: data.retrieve.list_of_available_files,
            tcpSocket: data.retrieve.tcp_socket,
          },
        ];
        setClientsDiscovered(newClientsList);
        enqueueSnackbar(`${searchedClient} found!`, {
          variant: "success" as VariantType,
        });
      });
  };

  const onSearchFile = () => {
    fetch("/searchfile", {
      method: "POST",
      body: JSON.stringify({
        fileName: searchedFile,
      }),
    })
      .then(async (response) => {
        if (!response.ok) {
          const result = await response.json();
          enqueueSnackbar(`${searchedFile} not found: ${result.searchfile}`, {
            variant: "error" as VariantType,
          });
          return Promise.reject();
        } else {
          return response.json();
        }
      })
      .then(async (data) => {
        const newFileList: File[] = [];
        data.searchfile.list_of_clients.forEach((c: any) => {
          const file: File = {
            fileName: searchedFile,
            clientName: c.name,
            ipAddress: c.ip_address,
            tcpSocket: c.tcp_socket,
          };
          newFileList.push(file);
        });
        setFilesDiscovered(newFileList);
        enqueueSnackbar(`${searchedFile} found!`, {
          variant: "success" as VariantType,
        });
      });
  };

  const onDownloadFile = (file: File) => {
    fetch("/download", {
      method: "POST",
      body: JSON.stringify({
        fileName: file.fileName,
        ipAddress: file.ipAddress,
        tcpSocket: file.tcpSocket,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.download === true) {
          enqueueSnackbar(`${file.fileName} downloaded successfully!`, {
            variant: "success" as VariantType,
          });
        } else {
          enqueueSnackbar(
            `Failed to download ${file.fileName}: ${data.download}`,
            {
              variant: "error" as VariantType,
            }
          );
        }
      });
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

  return (
    <>
      <div className="App">
        <Grid container spacing={3} style={{ paddingTop: "40px" }}>
          <Grid item xs>
            <Tooltip title="De-Register">
              <ArrowBackIcon
                style={{ color: "white", marginBottom: "40px" }}
                onClick={() => onBack()}
              />
            </Tooltip>
          </Grid>
          <Grid item xs={6}>
            <header className="App-page-header">
              Time to get transferring.
            </header>
          </Grid>
          <Grid item xs></Grid>
        </Grid>

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
                          <ListItemText
                            primary={
                              client.name +
                              "@" +
                              client.ipAddress +
                              ":" +
                              client.tcpSocket
                            }
                          />
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
                        key={file.fileName}
                        secondaryAction={
                          <IconButton>
                            <DownloadIcon
                              style={{ color: "white" }}
                              onClick={() => onDownloadFile(file)}
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
                            primary={
                              file.fileName +
                              ", " +
                              file.clientName +
                              "@" +
                              file.ipAddress +
                              ":" +
                              file.tcpSocket
                            }
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
