import {
  AppBar, Toolbar, Typography, Box,
  IconButton, Avatar, Chip, Badge,
} from "@mui/material";

import NotificationsNoneIcon from "@mui/icons-material/NotificationsNone";
import ApartmentIcon         from "@mui/icons-material/Apartment";

import ThemeToggle from "./ThemeToggle";
import { DRAWER_WIDTH } from "./Sidebar";

function Navbar() {
  const today = new Date().toLocaleDateString("en-GB", {
    weekday: "short", year: "numeric", month: "short", day: "numeric",
  });

  return (
    <AppBar
      elevation={0}
      sx={{
        width: `calc(100% - ${DRAWER_WIDTH}px)`,
        ml: `${DRAWER_WIDTH}px`,
        bgcolor: "background.paper",
        backdropFilter: "blur(12px)",
        borderBottom: "1px solid",
        borderColor: "divider",
        color: "text.primary",
        boxShadow: "none",
      }}
    >
      <Toolbar sx={{ gap: 1.5 }}>
        <ApartmentIcon sx={{ color: "#2563EB", mr: 1 }} />

        <Typography
          variant="h6"
          sx={{ fontWeight: 700, flexGrow: 1, color: "text.primary" }}
        >
          AI Smart Building
          <Typography component="span" variant="body2" sx={{ ml: 1, color: "#64748B", fontWeight: 400 }}>
            Optimization System
          </Typography>
        </Typography>

        <Chip
          label={today}
          size="small"
          sx={{ bgcolor: "#EFF6FF", color: "#2563EB", fontWeight: 600, mr: 1 }}
        />

        <Badge badgeContent={3} color="error">
          <IconButton size="small" sx={{ color: "#64748B" }}>
            <NotificationsNoneIcon />
          </IconButton>
        </Badge>

        <ThemeToggle />

        <Avatar
          sx={{
            width: 34, height: 34,
            background: "linear-gradient(135deg,#2563EB,#06B6D4)",
            fontSize: 14, fontWeight: 700, ml: 0.5,
          }}
        >
          A
        </Avatar>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
