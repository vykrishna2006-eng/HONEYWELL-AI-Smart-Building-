import { useEffect, useState } from "react";

import {
  Box,
  Typography,
  Paper,
  Stack,
  Avatar,
  Chip,
  Divider,
  CircularProgress,
  Grid,
} from "@mui/material";

import SmartToyIcon from "@mui/icons-material/SmartToy";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import SavingsIcon from "@mui/icons-material/Savings";
import BoltIcon from "@mui/icons-material/Bolt";
import TipsAndUpdatesIcon from "@mui/icons-material/TipsAndUpdates";

import DashboardLayout from "../layouts/DashboardLayout";
import { getRecommendation } from "../services/llmService";

function Recommendations() {
  const [recommendation, setRecommendation] = useState("");

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRecommendation();
  }, []);

  const loadRecommendation = async () => {
    try {
      const response = await getRecommendation();

      if (typeof response === "string") {
        setRecommendation(response);
      } else {
        setRecommendation(
          response.response ||
            response.recommendation ||
            response.message ||
            JSON.stringify(response, null, 2)
        );
      }
    } catch (err) {
      console.error(err);
      setRecommendation("Unable to load AI recommendation.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      {/* Header */}

      <Paper
        elevation={0}
        sx={{
          mb: 4,
          p: 4,
          borderRadius: 5,
          background: "linear-gradient(135deg,#2563EB,#06B6D4)",
          color: "white",
        }}
      >
        <Stack direction="row" spacing={3} alignItems="center">
          <Avatar
            sx={{
              width: 70,
              height: 70,
              bgcolor: "rgba(255,255,255,.25)",
            }}
          >
            <SmartToyIcon sx={{ fontSize: 40 }} />
          </Avatar>

          <Box>
            <Typography variant="h4" fontWeight={700}>
              AI Recommendation Assistant
            </Typography>

            <Typography sx={{ opacity: 0.9 }}>
              Gemini-powered intelligent optimisation engine
            </Typography>
          </Box>
        </Stack>
      </Paper>

      {/* KPI */}

      <Grid container spacing={3} mb={4}>
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
                color: "#22C55E",
              }}
            />

            <Typography variant="h4" fontWeight={700}>
              18%
            </Typography>

            <Typography color="text.secondary">
              Estimated Savings
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
            <BoltIcon
              sx={{
                fontSize: 45,
                color: "#2563EB",
              }}
            />

            <Typography variant="h4" fontWeight={700}>
              High
            </Typography>

            <Typography color="text.secondary">
              Optimisation Level
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
            <AutoAwesomeIcon
              sx={{
                fontSize: 45,
                color: "#8B5CF6",
              }}
            />

            <Typography variant="h4" fontWeight={700}>
              AI
            </Typography>

            <Typography color="text.secondary">
              Powered by Gemini
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* Recommendation */}

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
          spacing={2}
          alignItems="center"
          mb={3}
        >
          <Avatar
            sx={{
              bgcolor: "#2563EB",
            }}
          >
            <SmartToyIcon />
          </Avatar>

          <Box>
            <Typography variant="h5" fontWeight={700}>
              AI Generated Recommendation
            </Typography>

            <Typography color="text.secondary">
              Generated in real time
            </Typography>
          </Box>

          <Box flexGrow={1} />

          <Chip color="success" label="Live" />
        </Stack>

        <Divider sx={{ mb: 3 }} />

        {loading ? (
          <Box textAlign="center" py={6}>
            <CircularProgress />

            <Typography mt={2}>
              Gemini is analysing your building...
            </Typography>
          </Box>
        ) : (
          <Paper
            elevation={0}
            sx={{
              bgcolor: "#EFF6FF",
              p: 4,
              borderRadius: 4,
              borderLeft: "5px solid #2563EB",
            }}
          >
            <Stack
              direction="row"
              spacing={2}
              alignItems="flex-start"
            >
              <TipsAndUpdatesIcon
                sx={{
                  color: "#2563EB",
                  mt: 0.5,
                }}
              />

              <Typography
                sx={{
                  whiteSpace: "pre-wrap",
                  lineHeight: 2,
                }}
              >
                {recommendation}
              </Typography>
            </Stack>
          </Paper>
        )}
      </Paper>
    </DashboardLayout>
  );
}

export default Recommendations;