import { Box, CircularProgress } from "@mui/material";

function Loading() {
  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      sx={{ minHeight: "300px" }}
    >
      <CircularProgress size={50} />
    </Box>
  );
}

export default Loading;