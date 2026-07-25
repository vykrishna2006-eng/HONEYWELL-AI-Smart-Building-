import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  IconButton,
  Avatar,
  Chip,
} from "@mui/material";

import NotificationsNoneIcon from "@mui/icons-material/NotificationsNone";
import BusinessIcon from "@mui/icons-material/Business";

import ThemeToggle from "./ThemeToggle";

function Navbar() {
  const today = new Date().toLocaleDateString();

  return (
    <AppBar
      elevation={0}
      sx={{
        background:
          "linear-gradient(90deg,#2563EB,#06B6D4)",
        backdropFilter: "blur(10px)",
      }}
    >
      <Toolbar>

        <BusinessIcon sx={{ mr: 2 }} />

        <Typography
          variant="h6"
          sx={{
            fontWeight: 700,
            flexGrow: 1,
          }}
        >
          AI Smart Building Optimization System
        </Typography>

        <Chip
          label={today}
          sx={{
            mr: 3,
            bgcolor: "rgba(255,255,255,.2)",
            color: "white",
          }}
        />

        <IconButton color="inherit">
          <NotificationsNoneIcon />
        </IconButton>

        <ThemeToggle />

        <Avatar
          sx={{
            ml: 2,
            bgcolor: "#ffffff",
            color: "#2563EB",
            fontWeight: 700,
          }}
        >
          A
        </Avatar>

      </Toolbar>
    </AppBar>
  );
}

export default Navbar;