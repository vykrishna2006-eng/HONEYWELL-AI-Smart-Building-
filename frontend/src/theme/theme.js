import { createTheme } from "@mui/material/styles";

const getTheme = (mode) =>
  createTheme({
    palette: {
      mode,

      primary: {
        main: "#2563EB",
      },

      secondary: {
        main: "#06B6D4",
      },

      background: {
        default: mode === "light" ? "#F8FAFC" : "#0F172A",
        paper: mode === "light" ? "#FFFFFF" : "#1E293B",
      },

      text: {
        primary: mode === "light" ? "#1E293B" : "#F8FAFC",
        secondary: mode === "light" ? "#64748B" : "#CBD5E1",
      },
    },

    shape: {
      borderRadius: 18,
    },

    typography: {
      fontFamily: "'Poppins','Inter',sans-serif",

      h4: {
        fontWeight: 700,
      },

      h5: {
        fontWeight: 700,
      },

      h6: {
        fontWeight: 600,
      },
    },

    components: {
      MuiPaper: {
        styleOverrides: {
          root: {
            borderRadius: 18,
          },
        },
      },

      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: 12,
            textTransform: "none",
            fontWeight: 600,
          },
        },
      },
    },
  });

export default getTheme;