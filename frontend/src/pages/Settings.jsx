import { useState } from "react";

import {
  Avatar,
  Box,
  Button,
  Divider,
  FormControlLabel,
  Grid,
  Paper,
  Stack,
  Switch,
  TextField,
  Typography,
  Snackbar,
  Alert,
} from "@mui/material";

import PersonIcon from "@mui/icons-material/Person";
import NotificationsIcon from "@mui/icons-material/Notifications";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import ApartmentIcon from "@mui/icons-material/Apartment";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import SaveIcon from "@mui/icons-material/Save";

import DashboardLayout from "../layouts/DashboardLayout";

function Settings() {

  const [settings, setSettings] = useState({

    username: "Administrator",

    email: "admin@smartbuilding.ai",

    building: "Building A",

    notifications: true,

    darkMode: false,

    aiSuggestions: true,

  });

  const [open, setOpen] = useState(false);

  const handleSwitch = (field) => {

    setSettings((prev) => ({

      ...prev,

      [field]: !prev[field],

    }));

  };

  const handleChange = (field, value) => {

    setSettings((prev) => ({

      ...prev,

      [field]: value,

    }));

  };

  const saveSettings = () => {

    // API Call later

    setOpen(true);

  };

  return (

    <DashboardLayout>

      {/* Hero */}

      <Paper
        elevation={0}
        sx={{
          p: 4,
          mb: 4,
          borderRadius: 5,
          background:
            "linear-gradient(135deg,#2563EB,#06B6D4)",
          color: "white",
        }}
      >

        <Stack
          direction="row"
          spacing={3}
          alignItems="center"
        >

          <Avatar
            sx={{
              width: 70,
              height: 70,
              bgcolor: "rgba(255,255,255,.2)",
            }}
          >
            <PersonIcon sx={{ fontSize: 40 }} />
          </Avatar>

          <Box>

            <Typography
              variant="h4"
              fontWeight={700}
            >
              Settings
            </Typography>

            <Typography>
              Configure your Smart Building platform.
            </Typography>

          </Box>

        </Stack>

      </Paper>

      <Grid container spacing={3}>

        {/* Profile */}

        <Grid item xs={12} md={6}>

          <Paper
            elevation={0}
            sx={{
              p: 4,
              borderRadius: 5,
              border: "1px solid #E2E8F0",
            }}
          >

            <Stack
              direction="row"
              spacing={2}
              alignItems="center"
              mb={3}
            >

              <PersonIcon color="primary" />

              <Typography
                variant="h6"
                fontWeight={700}
              >
                User Profile
              </Typography>

            </Stack>

            <TextField
              fullWidth
              label="Username"
              value={settings.username}
              onChange={(e)=>
                handleChange(
                  "username",
                  e.target.value
                )
              }
              margin="normal"
            />

            <TextField
              fullWidth
              label="Email"
              value={settings.email}
              onChange={(e)=>
                handleChange(
                  "email",
                  e.target.value
                )
              }
              margin="normal"
            />

          </Paper>

        </Grid>

        {/* Building */}

        <Grid item xs={12} md={6}>

          <Paper
            elevation={0}
            sx={{
              p:4,
              borderRadius:5,
              border:"1px solid #E2E8F0",
            }}
          >

            <Stack
              direction="row"
              spacing={2}
              alignItems="center"
              mb={3}
            >

              <ApartmentIcon color="primary"/>

              <Typography
                variant="h6"
                fontWeight={700}
              >
                Building
              </Typography>

            </Stack>

            <TextField
              fullWidth
              label="Building Name"
              value={settings.building}
              onChange={(e)=>
                handleChange(
                  "building",
                  e.target.value
                )
              }
            />

          </Paper>

        </Grid>

        {/* Preferences */}

        <Grid item xs={12}>

          <Paper
            elevation={0}
            sx={{
              p:4,
              borderRadius:5,
              border:"1px solid #E2E8F0",
            }}
          >

            <Typography
              variant="h6"
              fontWeight={700}
            >
              Preferences
            </Typography>

            <Divider sx={{my:3}}/>

            <Stack spacing={2}>

              <FormControlLabel
                control={
                  <Switch
                    checked={settings.notifications}
                    onChange={()=>
                      handleSwitch("notifications")
                    }
                  />
                }
                label={
                  <Stack direction="row" spacing={1}>
                    <NotificationsIcon/>
                    <Typography>
                      Enable Notifications
                    </Typography>
                  </Stack>
                }
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={settings.aiSuggestions}
                    onChange={()=>
                      handleSwitch("aiSuggestions")
                    }
                  />
                }
                label={
                  <Stack direction="row" spacing={1}>
                    <SmartToyIcon/>
                    <Typography>
                      AI Recommendations
                    </Typography>
                  </Stack>
                }
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={settings.darkMode}
                    onChange={()=>
                      handleSwitch("darkMode")
                    }
                  />
                }
                label={
                  <Stack direction="row" spacing={1}>
                    <DarkModeIcon/>
                    <Typography>
                      Dark Mode
                    </Typography>
                  </Stack>
                }
              />

            </Stack>

          </Paper>

        </Grid>

      </Grid>

      <Box
        mt={4}
        display="flex"
        justifyContent="flex-end"
      >

        <Button
          variant="contained"
          size="large"
          startIcon={<SaveIcon/>}
          onClick={saveSettings}
        >
          Save Settings
        </Button>

      </Box>

      <Snackbar
        open={open}
        autoHideDuration={3000}
        onClose={()=>setOpen(false)}
      >
        <Alert
          severity="success"
          variant="filled"
        >
          Settings Saved Successfully
        </Alert>
      </Snackbar>

    </DashboardLayout>

  );

}

export default Settings;