import { useState } from "react";
import {
  Grid, Paper, TextField, Button, Typography,
  Alert, CircularProgress, Box, Stack, Avatar,
  Chip, Divider, LinearProgress,
} from "@mui/material";

import QueryStatsIcon    from "@mui/icons-material/QueryStats";
import BoltIcon          from "@mui/icons-material/Bolt";
import ThermostatIcon    from "@mui/icons-material/Thermostat";
import SavingsIcon       from "@mui/icons-material/Savings";
import CheckCircleIcon   from "@mui/icons-material/CheckCircle";
import TipsAndUpdatesIcon from "@mui/icons-material/TipsAndUpdates";

import DashboardLayout   from "../layouts/DashboardLayout";
import PredictionTable   from "../components/PredictionTable";
import PredictionHistoryChart from "../components/PredictionHistoryChart";
import { predict }       from "../services/predictionService";

const FIELDS = [
  { name: "temperature", label: "Indoor Temperature (°C)", placeholder: "e.g. 22.5" },
  { name: "humidity",    label: "Humidity (%)",            placeholder: "e.g. 55"   },
  { name: "co2",         label: "CO₂ (ppm)",               placeholder: "e.g. 600"  },
  { name: "occupancy",   label: "Occupancy",               placeholder: "e.g. 10"   },
  { name: "hvac_temp",   label: "HVAC Setpoint (°C)",      placeholder: "e.g. 21"   },
];

export default function Predictions() {
  const [form,    setForm]    = useState({ temperature:"", humidity:"", co2:"", occupancy:"", hvac_temp:"" });
  const [result,  setResult]  = useState(null);
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState("");

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value === "" ? "" : Number(e.target.value) });

  const handleSubmit = async () => {
    if (Object.values(form).some((v) => v === "")) {
      setError("Please fill in all fields before predicting.");
      return;
    }
    try {
      setLoading(true);
      setError("");
      setResult(await predict(form));
    } catch {
      setError("Prediction failed. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      {/* Header */}
      <Stack direction="row" alignItems="center" spacing={1.5} mb={4}>
        <QueryStatsIcon sx={{ color: "#2563EB", fontSize: 32 }} />
        <Box>
          <Typography variant="h4" fontWeight={800}>AI Prediction</Typography>
          <Typography variant="body2" color="text.secondary">
            Enter sensor readings to get ML energy & comfort predictions
          </Typography>
        </Box>
      </Stack>

      <Grid container spacing={3}>
        {/* Form */}
        <Grid item xs={12} lg={5}>
          <Paper
            className="hover-lift fade-in"
            sx={{ p: 4, border: "1px solid #E2E8F0" }}
          >
            <Typography variant="h6" fontWeight={700} mb={3}>Sensor Inputs</Typography>

            <Grid container spacing={2}>
              {FIELDS.map((f) => (
                <Grid item xs={12} sm={6} key={f.name}>
                  <TextField
                    fullWidth
                    type="number"
                    label={f.label}
                    name={f.name}
                    value={form[f.name]}
                    onChange={handleChange}
                    placeholder={f.placeholder}
                    size="small"
                  />
                </Grid>
              ))}
            </Grid>

            {error && (
              <Alert severity="error" sx={{ mt: 2, borderRadius: 2 }}>{error}</Alert>
            )}

            <Box mt={3}>
              <Button
                fullWidth
                variant="contained"
                size="large"
                onClick={handleSubmit}
                disabled={loading}
                startIcon={loading ? <CircularProgress size={18} color="inherit" /> : <QueryStatsIcon />}
              >
                {loading ? "Predicting…" : "Run Prediction"}
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Result */}
        <Grid item xs={12} lg={7}>
          {result ? (
            <Paper
              className="hover-lift fade-in"
              sx={{ p: 4, border: "1px solid #E2E8F0" }}
            >
              <Stack direction="row" spacing={2} alignItems="center" mb={3}>
                <Avatar sx={{ bgcolor: "#22C55E" }}><CheckCircleIcon /></Avatar>
                <Box>
                  <Typography variant="h6" fontWeight={700}>Prediction Result</Typography>
                  <Typography variant="body2" color="text.secondary">
                    RandomForest ML model output
                  </Typography>
                </Box>
                <Box flexGrow={1} />
                <Chip label="Success" color="success" size="small" />
              </Stack>

              <Divider sx={{ mb: 3 }} />

              <Grid container spacing={2} mb={3}>
                {[
                  { label:"Energy Consumption", val:`${Number(result.predicted_energy_kWh).toFixed(3)} kWh`,  icon:<BoltIcon />,       color:"#2563EB", bg:"#EFF6FF" },
                  { label:"Comfort Score",       val:Number(result.predicted_comfort_score).toFixed(4),       icon:<ThermostatIcon />, color:"#22C55E", bg:"#F0FDF4" },
                  { label:"HVAC Setpoint",       val:`${Number(result.recommended_hvac_setpoint).toFixed(1)}°C`, icon:<ThermostatIcon />, color:"#EA580C", bg:"#FFF7ED" },
                  { label:"Expected Savings",    val:`${Number(result.expected_energy_saving_percent).toFixed(1)}%`, icon:<SavingsIcon />,  color:"#8B5CF6", bg:"#F5F3FF" },
                ].map((m) => (
                  <Grid item xs={12} sm={6} key={m.label}>
                    <Paper elevation={0} sx={{ p: 2, bgcolor: m.bg, borderRadius: 3 }}>
                      <Stack direction="row" spacing={1.5} alignItems="center">
                        <Box sx={{ color: m.color }}>{m.icon}</Box>
                        <Box>
                          <Typography variant="caption" color="text.secondary">{m.label}</Typography>
                          <Typography variant="h6" fontWeight={800} sx={{ color: m.color }}>{m.val}</Typography>
                        </Box>
                      </Stack>
                    </Paper>
                  </Grid>
                ))}
              </Grid>

              {/* Progress bars */}
              <Box mb={2}>
                <Stack direction="row" justifyContent="space-between" mb={0.5}>
                  <Typography variant="body2" fontWeight={600}>Confidence</Typography>
                  <Typography variant="body2" color="text.secondary">High</Typography>
                </Stack>
                <LinearProgress
                  variant="determinate"
                  value={95}
                  sx={{ height: 8, borderRadius: 20, "& .MuiLinearProgress-bar": { bgcolor: "#2563EB" } }}
                />
              </Box>

              {result.recommendations?.length > 0 && (
                <Paper elevation={0} sx={{ bgcolor:"#EFF6FF", p:2.5, borderRadius:3, borderLeft:"4px solid #2563EB" }}>
                  <Stack direction="row" spacing={1} alignItems="flex-start">
                    <TipsAndUpdatesIcon sx={{ color:"#2563EB", mt:0.3, flexShrink:0 }} />
                    <Box>
                      <Typography variant="subtitle2" fontWeight={700} mb={0.5}>
                        AI Recommendations
                      </Typography>
                      <ul style={{ paddingLeft: 18, margin: 0 }}>
                        {result.recommendations.map((r, i) => (
                          <li key={i}>
                            <Typography variant="body2" lineHeight={2}>{r}</Typography>
                          </li>
                        ))}
                      </ul>
                    </Box>
                  </Stack>
                </Paper>
              )}
            </Paper>
          ) : (
            <Paper
              className="fade-in"
              sx={{
                p: 6, border: "1px solid #E2E8F0",
                display: "flex", flexDirection:"column",
                alignItems:"center", justifyContent:"center",
                height: "100%", minHeight: 300,
                background: "linear-gradient(145deg,#fff,#f8fafc)",
              }}
            >
              <QueryStatsIcon sx={{ fontSize: 64, color:"#CBD5E1", mb:2 }} />
              <Typography variant="h6" color="text.secondary" fontWeight={600}>
                Enter sensor values to run a prediction
              </Typography>
              <Typography variant="body2" color="text.secondary" mt={1} textAlign="center">
                The ML model will predict energy consumption, comfort score,
                optimal HVAC setpoint and expected savings.
              </Typography>
            </Paper>
          )}
        </Grid>
      </Grid>

      {/* History Chart */}
      <Box mt={4}>
        <PredictionHistoryChart />
      </Box>

      {/* History Table */}
      <Box mt={3}>
        <PredictionTable />
      </Box>
    </DashboardLayout>
  );
}
