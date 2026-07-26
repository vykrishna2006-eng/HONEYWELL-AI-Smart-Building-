import { useState } from "react";
import {
  Avatar, Box, Button, Divider, FormControlLabel,
  Grid, Paper, Stack, Switch, TextField, Typography,
  Snackbar, Alert,
} from "@mui/material";

import PersonIcon       from "@mui/icons-material/Person";
import NotificationsIcon from "@mui/icons-material/Notifications";
import SmartToyIcon     from "@mui/icons-material/SmartToy";
import ApartmentIcon    from "@mui/icons-material/Apartment";
import DarkModeIcon     from "@mui/icons-material/DarkMode";
import SaveIcon         from "@mui/icons-material/Save";
import SettingsIcon     from "@mui/icons-material/Settings";

import DashboardLayout  from "../layouts/DashboardLayout";
import { useThemeMode } from "../contexts/ThemeContext";

export default function Settings() {
  const { toggleTheme, mode } = useThemeMode();

  const [settings, setSettings] = useState({
    username:      "Administrator",
    email:         "admin@smartbuilding.ai",
    building:      "Building A",
    notifications: true,
    aiSuggestions: true,
    darkMode:      mode === "dark",
  });

  const [open, setOpen] = useState(false);

  const handleSwitch = (field) => {
    if (field === "darkMode") toggleTheme();
    setSettings((p) => ({ ...p, [field]: !p[field] }));
  };

  const handleChange = (field, value) =>
    setSettings((p) => ({ ...p, [field]: value }));

  return (
    <DashboardLayout>
      {/* Hero */}
      <Paper
        className="fade-in"
        sx={{
          p: { xs:3, md:4 }, mb:4,
          background: "linear-gradient(135deg,#2563EB,#06B6D4)",
          color: "white",
        }}
      >
        <Stack direction="row" spacing={3} alignItems="center">
          <Avatar sx={{ width:70, height:70, bgcolor:"rgba(255,255,255,.2)" }}>
            <SettingsIcon sx={{ fontSize:40 }} />
          </Avatar>
          <Box>
            <Typography variant="h4" fontWeight={800}>Settings</Typography>
            <Typography sx={{ opacity:0.85 }}>Configure your AI Smart Building platform</Typography>
          </Box>
        </Stack>
      </Paper>

      <Grid container spacing={3}>
        {/* Profile */}
        <Grid item xs={12} md={6}>
          <Paper className="hover-lift fade-in" sx={{ p:4, border:"1px solid #E2E8F0" }}>
            <Stack direction="row" spacing={2} alignItems="center" mb={3}>
              <PersonIcon color="primary" />
              <Typography variant="h6" fontWeight={700}>User Profile</Typography>
            </Stack>
            <TextField
              fullWidth label="Username" margin="normal" size="small"
              value={settings.username}
              onChange={(e) => handleChange("username", e.target.value)}
            />
            <TextField
              fullWidth label="Email Address" margin="normal" size="small"
              value={settings.email}
              onChange={(e) => handleChange("email", e.target.value)}
            />
          </Paper>
        </Grid>

        {/* Building */}
        <Grid item xs={12} md={6}>
          <Paper className="hover-lift fade-in" sx={{ p:4, border:"1px solid #E2E8F0" }}>
            <Stack direction="row" spacing={2} alignItems="center" mb={3}>
              <ApartmentIcon color="primary" />
              <Typography variant="h6" fontWeight={700}>Building</Typography>
            </Stack>
            <TextField
              fullWidth label="Building Name" size="small"
              value={settings.building}
              onChange={(e) => handleChange("building", e.target.value)}
            />
          </Paper>
        </Grid>

        {/* Preferences */}
        <Grid item xs={12}>
          <Paper className="hover-lift fade-in" sx={{ p:4, border:"1px solid #E2E8F0" }}>
            <Typography variant="h6" fontWeight={700}>Preferences</Typography>
            <Divider sx={{ my:2.5 }} />
            <Stack spacing={2.5}>
              {[
                { field:"notifications", icon:<NotificationsIcon />, label:"Enable Notifications" },
                { field:"aiSuggestions",  icon:<SmartToyIcon />,       label:"AI Recommendations"   },
                { field:"darkMode",       icon:<DarkModeIcon />,        label:"Dark Mode"             },
              ].map(({ field, icon, label }) => (
                <FormControlLabel
                  key={field}
                  control={
                    <Switch
                      checked={settings[field]}
                      onChange={() => handleSwitch(field)}
                      color="primary"
                    />
                  }
                  label={
                    <Stack direction="row" spacing={1.5} alignItems="center">
                      <Box sx={{ color:"text.secondary" }}>{icon}</Box>
                      <Typography fontWeight={500}>{label}</Typography>
                    </Stack>
                  }
                />
              ))}
            </Stack>
          </Paper>
        </Grid>
      </Grid>

      <Box mt={4} display="flex" justifyContent="flex-end">
        <Button
          variant="contained"
          size="large"
          startIcon={<SaveIcon />}
          onClick={() => setOpen(true)}
        >
          Save Settings
        </Button>
      </Box>

      <Snackbar open={open} autoHideDuration={3000} onClose={() => setOpen(false)}>
        <Alert severity="success" variant="filled" sx={{ borderRadius: 3 }}>
          Settings saved successfully
        </Alert>
      </Snackbar>
    </DashboardLayout>
  );
}
