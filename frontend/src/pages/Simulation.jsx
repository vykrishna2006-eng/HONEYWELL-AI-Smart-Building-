import { useState } from "react";

import {
  Box,
  Paper,
  Typography,
  Grid,
  Button,
  Stack,
  Chip,
  LinearProgress,
  CircularProgress,
  Divider,
} from "@mui/material";

import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import BoltIcon from "@mui/icons-material/Bolt";
import ThermostatIcon from "@mui/icons-material/Thermostat";
import SavingsIcon from "@mui/icons-material/Savings";
import SmartToyIcon from "@mui/icons-material/SmartToy";

import DashboardLayout from "../layouts/DashboardLayout";
import { runSimulation } from "../services/simulationService";

function Simulation() {

  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState(null);

  const startSimulation = async () => {

    setLoading(true);

    try {

      const data = await runSimulation();

      setResult(data);

    } catch (err) {

      console.log(err);

    }

    setLoading(false);

  };

  return (

    <DashboardLayout>

      {/* Header */}

      <Paper
        elevation={0}
        sx={{
          p: 4,
          mb: 4,
          borderRadius: 5,
          background:
            "linear-gradient(135deg,#2563EB,#06B6D4)",
          color: "white",
        }}
      >

        <Typography
          variant="h4"
          fontWeight={700}
        >
          Building Simulation
        </Typography>

        <Typography mt={1}>
          Run AI-powered building optimisation simulations
          using the latest sensor readings.
        </Typography>

      </Paper>

      {/* Control Panel */}

      <Paper
        elevation={0}
        sx={{
          p: 4,
          borderRadius: 5,
          border: "1px solid #E2E8F0",
        }}
      >

        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
          flexWrap="wrap"
          gap={2}
        >

          <Box>

            <Typography
              variant="h5"
              fontWeight={700}
            >
              Simulation Control
            </Typography>

            <Typography
              color="text.secondary"
            >
              Execute a new optimisation cycle.
            </Typography>

          </Box>

          <Button
            variant="contained"
            size="large"
            startIcon={<PlayArrowIcon />}
            onClick={startSimulation}
            disabled={loading}
          >
            Start Simulation
          </Button>

        </Stack>

        {

          loading && (

            <Box mt={4}>

              <Typography mb={1}>
                Running Simulation...
              </Typography>

              <LinearProgress />

            </Box>

          )

        }

      </Paper>

      {

        loading && (

          <Box
            textAlign="center"
            py={8}
          >

            <CircularProgress />

            <Typography mt={2}>
              AI is analysing building conditions...
            </Typography>

          </Box>

        )

      }

      {

        result && (

          <>

            <Grid
              container
              spacing={3}
              mt={2}
            >

              <Grid item xs={12} md={4}>

                <Paper
                  elevation={0}
                  sx={{
                    p: 3,
                    borderRadius: 5,
                    textAlign: "center",
                    border: "1px solid #E2E8F0",
                  }}
                >

                  <BoltIcon
                    sx={{
                      fontSize: 45,
                      color: "#2563EB",
                    }}
                  />

                  <Typography
                    variant="h4"
                    fontWeight={700}
                    mt={2}
                  >
                    {result.energy_prediction}
                  </Typography>

                  <Typography color="text.secondary">
                    Energy Prediction
                  </Typography>

                </Paper>

              </Grid>

              <Grid item xs={12} md={4}>

                <Paper
                  elevation={0}
                  sx={{
                    p: 3,
                    borderRadius: 5,
                    textAlign: "center",
                    border: "1px solid #E2E8F0",
                  }}
                >

                  <ThermostatIcon
                    sx={{
                      fontSize: 45,
                      color: "#22C55E",
                    }}
                  />

                  <Typography
                    variant="h4"
                    fontWeight={700}
                    mt={2}
                  >
                    {result.comfort_score}%
                  </Typography>

                  <Typography color="text.secondary">
                    Comfort Score
                  </Typography>

                </Paper>

              </Grid>

              <Grid item xs={12} md={4}>

                <Paper
                  elevation={0}
                  sx={{
                    p: 3,
                    borderRadius: 5,
                    textAlign: "center",
                    border: "1px solid #E2E8F0",
                  }}
                >

                  <SavingsIcon
                    sx={{
                      fontSize: 45,
                      color: "#F59E0B",
                    }}
                  />

                  <Typography
                    variant="h4"
                    fontWeight={700}
                    mt={2}
                  >
                    {result.expected_savings}%
                  </Typography>

                  <Typography color="text.secondary">
                    Expected Savings
                  </Typography>

                </Paper>

              </Grid>

            </Grid>

            <Paper
              elevation={0}
              sx={{
                mt: 4,
                p: 4,
                borderRadius: 5,
                border: "1px solid #E2E8F0",
              }}
            >

              <Stack
                direction="row"
                spacing={2}
                alignItems="center"
              >

                <SmartToyIcon
                  color="primary"
                />

                <Typography
                  variant="h5"
                  fontWeight={700}
                >
                  Simulation Summary
                </Typography>

                <Box flexGrow={1} />

                <Chip
                  icon={<CheckCircleIcon />}
                  label="Completed"
                  color="success"
                />

              </Stack>

              <Divider sx={{ my: 3 }} />

              <Typography
                lineHeight={2}
                color="text.secondary"
              >
                {result.summary}
              </Typography>

            </Paper>

          </>

        )

      }

    </DashboardLayout>

  );

}

export default Simulation;