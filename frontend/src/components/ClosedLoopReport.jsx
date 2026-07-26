import { useEffect, useState } from "react";
import {
  Paper, Typography, Box, Stack, Chip,
  Divider, CircularProgress, Grid,
} from "@mui/material";
import BoltIcon from "@mui/icons-material/Bolt";
import { getClosedLoopReport } from "../services/simulationService";

export default function ClosedLoopReport() {
  const [history, setHistory] = useState(null);
  const [error,   setError]   = useState(false);

  useEffect(() => { load(); }, []);

  const load = async () => {
    try {
      setHistory(await getClosedLoopReport());
    } catch {
      setError(true);
    }
  };

  if (error) return null;

  if (!history) {
    return (
      <Paper sx={{ p:4, textAlign:"center", border:"1px solid #E2E8F0" }}>
        <CircularProgress size={24} />
        <Typography mt={2} color="text.secondary">Loading closed-loop report…</Typography>
      </Paper>
    );
  }

  const first = history[0]?.energy?.total_energy_kwh;
  const last  = history[history.length - 1]?.energy?.total_energy_kwh;
  const savingsPct =
    first && last ? (((first - last) / first) * 100).toFixed(2) : null;

  return (
    <Paper
      className="fade-in"
      sx={{ p:4, border:"1px solid #E2E8F0", mt:4 }}
    >
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
        <Stack direction="row" spacing={1.5} alignItems="center">
          <BoltIcon color="primary" />
          <Typography variant="h5" fontWeight={700}>
            AI Closed-Loop Optimization Results
          </Typography>
        </Stack>
        {savingsPct && (
          <Chip
            label={`${savingsPct}% Energy Reduction`}
            color={savingsPct > 0 ? "success" : "default"}
            sx={{ fontWeight:700 }}
          />
        )}
      </Stack>

      <Divider sx={{ mb:3 }} />

      {/* Savings Chart Image */}
      <Box
        component="img"
        src="http://127.0.0.1:8000/simulation/closed-loop-chart"
        alt="Closed-loop savings chart"
        onError={(e) => { e.target.style.display = "none"; }}
        sx={{ width:"100%", borderRadius:3, mb:3, maxHeight:400, objectFit:"contain" }}
      />

      {/* Iteration Cards */}
      <Grid container spacing={2}>
        {history.map((h) => (
          <Grid item xs={12} md={6} key={h.iteration}>
            <Paper
              elevation={0}
              sx={{ p:2.5, bgcolor:"#F8FAFC", borderRadius:3, border:"1px solid #E2E8F0" }}
            >
              <Stack direction="row" justifyContent="space-between" alignItems="center" mb={0.5}>
                <Typography fontWeight={700} variant="subtitle1">
                  Iteration {h.iteration}
                </Typography>
                <Chip
                  label={`${Number(h.energy?.total_energy_kwh).toFixed(3)} kWh`}
                  size="small"
                  color="primary"
                  variant="outlined"
                />
              </Stack>
              <Typography variant="body2" color="text.secondary">
                Cooling {h.applied_cooling_setpoint_c}°C · Heating {h.applied_heating_setpoint_c}°C
              </Typography>
              <Typography variant="body2" mt={1} sx={{ lineHeight:1.7 }}>
                {h.decision?.reason}
              </Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Paper>
  );
}
