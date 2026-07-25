import { IconButton } from "@mui/material";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import LightModeIcon from "@mui/icons-material/LightMode";

import { useThemeMode } from "../contexts/ThemeContext";

function ThemeToggle() {

  const { mode, toggleTheme } = useThemeMode();

  return (
    <IconButton
      color="inherit"
      onClick={toggleTheme}
    >
      {mode === "light" ? <DarkModeIcon /> : <LightModeIcon />}
    </IconButton>
  );
}

export default ThemeToggle;