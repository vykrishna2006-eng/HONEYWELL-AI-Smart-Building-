import { createTheme } from "@mui/material/styles";

const getTheme = (mode) =>
  createTheme({
    palette: {
      mode,
      primary:    { main: "#2563EB" },
      secondary:  { main: "#06B6D4" },
      success:    { main: "#22C55E" },
      warning:    { main: "#F59E0B" },
      error:      { main: "#EF4444" },
      background: {
        default: mode === "light" ? "#F1F5F9" : "#0A0F1E",
        paper:   mode === "light" ? "#FFFFFF"  : "#111827",
      },
      text: {
        primary:   mode === "light" ? "#0F172A" : "#F1F5F9",
        secondary: mode === "light" ? "#64748B" : "#94A3B8",
      },
    },
    shape: { borderRadius: 16 },
    typography: {
      fontFamily: "'Poppins','Inter',sans-serif",
      h3: { fontWeight: 800 },
      h4: { fontWeight: 700 },
      h5: { fontWeight: 700 },
      h6: { fontWeight: 600 },
    },
    components: {
      MuiPaper: {
        defaultProps: { elevation: 0 },
        styleOverrides: {
          root: {
            borderRadius: 20,
            backgroundImage: "none",
          },
        },
      },
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: 12,
            textTransform: "none",
            fontWeight: 600,
            paddingLeft: 20,
            paddingRight: 20,
          },
        },
      },
      MuiChip: {
        styleOverrides: { root: { fontWeight: 600 } },
      },
      MuiTextField: {
        styleOverrides: {
          root: { "& .MuiOutlinedInput-root": { borderRadius: 12 } },
        },
      },
    },
  });

export default getTheme;
