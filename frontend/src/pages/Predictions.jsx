import { useState } from "react";
import {
  Grid,
  Paper,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
  Box,
} from "@mui/material";

import DashboardLayout from "../layouts/DashboardLayout";
import Notification from "../components/NotificationDrawer";
import { predict } from "../services/predictionService";

function Predictions() {
  const [form, setForm] = useState({
    temperature: "",
    humidity: "",
    co2: "",
    occupancy: "",
    hvac_temp: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [notification, setNotification] = useState({
    open: false,
    severity: "success",
    message: "",
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]:
        e.target.value === "" ? "" : Number(e.target.value),
    });
  };

  const handleSubmit = async () => {
    if (
      form.temperature === "" ||
      form.humidity === "" ||
      form.co2 === "" ||
      form.occupancy === "" ||
      form.hvac_temp === ""
    ) {
      setNotification({
        open: true,
        severity: "warning",
        message: "Please fill all fields.",
      });
      return;
    }

    try {
      setLoading(true);
      setError("");

      const response = await predict(form);

      setResult(response);

      setNotification({
        open: true,
        severity: "success",
        message: "Prediction completed successfully!",
      });
    } catch (err) {
      console.error(err);

      setError("Prediction Failed");

      setNotification({
        open: true,
        severity: "error",
        message: "Prediction Failed!",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <Typography variant="h4" mb={4}>
        AI Prediction
      </Typography>

      <Paper
        elevation={4}
        sx={{
          p: 4,
          borderRadius: 3,
        }}
      >
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              type="number"
              label="Temperature (°C)"
              name="temperature"
              value={form.temperature}
              onChange={handleChange}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              type="number"
              label="Humidity (%)"
              name="humidity"
              value={form.humidity}
              onChange={handleChange}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              type="number"
              label="CO₂ (ppm)"
              name="co2"
              value={form.co2}
              onChange={handleChange}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              type="number"
              label="Occupancy"
              name="occupancy"
              value={form.occupancy}
              onChange={handleChange}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              type="number"
              label="HVAC Temperature (°C)"
              name="hvac_temp"
              value={form.hvac_temp}
              onChange={handleChange}
            />
          </Grid>
        </Grid>

        <Box mt={4}>
          <Button
            variant="contained"
            size="large"
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? (
              <CircularProgress size={24} color="inherit" />
            ) : (
              "Predict"
            )}
          </Button>
        </Box>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mt: 3 }}>
          {error}
        </Alert>
      )}

      {result && (
        <Paper
          elevation={4}
          sx={{
            mt: 4,
            p: 3,
            borderRadius: 3,
          }}
        >
          <Typography variant="h5" gutterBottom>
            Prediction Result
          </Typography>

          <Typography mt={2}>
            <strong>Energy Consumption:</strong>{" "}
            {result.predicted_energy_kWh} kWh
          </Typography>

          <Typography mt={1}>
            <strong>Comfort Score:</strong>{" "}
            {result.predicted_comfort_score}%
          </Typography>

          <Typography mt={1}>
            <strong>Recommended HVAC Setpoint:</strong>{" "}
            {result.recommended_hvac_setpoint}°C
          </Typography>

          <Typography mt={1}>
            <strong>Expected Savings:</strong>{" "}
            {result.expected_energy_saving_percent}%
          </Typography>

          <Typography mt={1}>
            <strong>Recommendations:</strong>
            <ul>
              {result.recommendations?.map((rec, i) => (
                <li key={i}>{rec}</li>
              ))}
            </ul>
          </Typography>
        </Paper>
      )}

      <Notification
        open={notification.open}
        severity={notification.severity}
        message={notification.message}
        onClose={() =>
          setNotification({
            ...notification,
            open: false,
          })
        }
      />
    </DashboardLayout>
  );
}

export default Predictions;