import { useEffect, useState } from "react";

import {
  Paper,
  Typography,
  Box,
  Stack,
  Chip,
  Divider,
  CircularProgress,
} from "@mui/material";

import { getClosedLoopReport } from "../services/simulationService";

function ClosedLoopReport() {
  const [history, setHistory] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    load();
  }, []);

  const load = async () => {
    try {
      const data = await getClosedLoopReport();
      setHistory(data);
    } catch (err) {
      console.log(err);
      setError(true);
    }
  };

  if (error) {
    return null;
  }

  if (!history) {
    return (
      <Paper sx={{ p: 4, borderRadius: 4, textAlign: "center" }}>
        <CircularProgress size={24} />
      </Paper>
    );
  }

  const first = history[0]?.energy?.total_energy_kwh;
  const last = history[history.length - 1]?.energy?.total_energy_kwh;

  const savingsPct =
    first && last ? (((first - last) / first) * 100).toFixed(2) : null;

  return (
    <Paper
      elevation={0}
      sx={{
        p: 4,
        borderRadius: 5,
        border: "1px solid #E2E8F0",
        mt: 4,
      }}
    >
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Typography variant="h5" fontWeight={700}>
          AI Closed-Loop Optimization Results
        </Typography>

        {savingsPct && (
          <Chip
            label={`${savingsPct}% Energy Reduction`}
            color={savingsPct > 0 ? "success" : "default"}
            sx={{ fontWeight: 700 }}
          />
        )}
      </Stack>

      <Divider sx={{ my: 3 }} />

      <Box
        component="img"
        src="http://127.0.0.1:8000/simulation/closed-loop-chart"
        alt="Closed-loop savings chart"
        sx={{ width: "100%", borderRadius: 2, mb: 3 }}
      />

      <Stack spacing={2}>
        {history.map((h) => (
          <Paper
            key={h.iteration}
            elevation={0}
            sx={{ p: 2, bgcolor: "#F8FAFC", borderRadius: 3 }}
          >
            <Typography fontWeight={700}>
              Iteration {h.iteration} — {h.energy.total_energy_kwh} kWh
            </Typography>
            <Typography variant="body2" color="text.secondary" mt={0.5}>
              Applied: Cooling {h.applied_cooling_setpoint_c}°C / Heating{" "}
              {h.applied_heating_setpoint_c}°C
            </Typography>
            <Typography variant="body2" mt={1}>
              {h.decision.reason}
            </Typography>
          </Paper>
        ))}
      </Stack>
    </Paper>
  );
}

export default ClosedLoopReport;