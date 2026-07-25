import { useEffect, useMemo, useState } from "react";

import {
  Paper,
  Typography,
  Box,
  Chip,
  TextField,
  InputAdornment,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  CircularProgress,
} from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";
import QueryStatsIcon from "@mui/icons-material/QueryStats";

import { getPredictions } from "../services/predictionService";

function PredictionTable() {

  const [predictions, setPredictions] = useState([]);

  const [loading, setLoading] = useState(true);

  const [search, setSearch] = useState("");

  const [page, setPage] = useState(0);

  const [rowsPerPage, setRowsPerPage] = useState(5);

  useEffect(() => {

    loadPredictions();

  }, []);

  const loadPredictions = async () => {

    try {

      const data = await getPredictions();

      setPredictions(data);

    } catch (err) {

      console.log(err);

    } finally {

      setLoading(false);

    }

  };

  const filteredData = useMemo(() => {

    return predictions.filter((item) =>
      JSON.stringify(item)
        .toLowerCase()
        .includes(search.toLowerCase())
    );

  }, [predictions, search]);

  const paginatedData = filteredData.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  return (

    <Paper
      elevation={0}
      sx={{
        mt: 3,
        p: 3,
        borderRadius: 5,
        border: "1px solid #E2E8F0",
        background:
          "linear-gradient(145deg,#ffffff,#f8fafc)",
      }}
    >

      <Box
        display="flex"
        justifyContent="space-between"
        alignItems="center"
        mb={3}
        flexWrap="wrap"
        gap={2}
      >

        <Box>

          <Typography
            variant="h5"
            fontWeight={700}
          >
            Prediction History
          </Typography>

          <Typography
            color="text.secondary"
          >
            Machine Learning Prediction Results
          </Typography>

        </Box>

        <TextField

          size="small"

          placeholder="Search..."

          value={search}

          onChange={(e) => setSearch(e.target.value)}

          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}

          sx={{
            width: 280,
          }}

        />

      </Box>

      {

        loading ?

          <Box
            display="flex"
            justifyContent="center"
            py={8}
          >

            <CircularProgress />

          </Box>

          :

          <>

            <TableContainer>

              <Table>

                <TableHead>

                  <TableRow
                    sx={{
                      bgcolor: "#EFF6FF",
                    }}
                  >

                    {
                      filteredData.length > 0 &&
                      Object.keys(filteredData[0]).map((key) => (

                        <TableCell
                          key={key}
                          sx={{
                            fontWeight: 700,
                            textTransform: "capitalize",
                          }}
                        >
                          {key.replaceAll("_", " ")}
                        </TableCell>

                      ))
                    }

                  </TableRow>

                </TableHead>

                <TableBody>

                  {

                    paginatedData.map((row, index) => (

                      <TableRow
                        key={index}
                        hover
                        sx={{
                          transition: ".3s",

                          "&:hover": {

                            bgcolor: "#F8FAFC",

                          },
                        }}
                      >

                        {

                          Object.entries(row).map(([key, value], i) => (

                            <TableCell key={i}>

                              {

                                typeof value === "number"

                                  ?

                                  Number(value).toFixed(2)

                                  :

                                  key.toLowerCase().includes("status")

                                    ?

                                    <Chip
                                      icon={<QueryStatsIcon />}
                                      color="success"
                                      label={value}
                                      size="small"
                                    />

                                    :

                                    String(value)

                              }

                            </TableCell>

                          ))

                        }

                      </TableRow>

                    ))

                  }

                </TableBody>

              </Table>

            </TableContainer>

            <TablePagination

              rowsPerPageOptions={[5, 10, 20]}

              component="div"

              count={filteredData.length}

              page={page}

              rowsPerPage={rowsPerPage}

              onPageChange={(e, newPage) => setPage(newPage)}

              onRowsPerPageChange={(e) => {

                setRowsPerPage(parseInt(e.target.value, 10));

                setPage(0);

              }}

            />

          </>

      }

    </Paper>

  );

}

export default PredictionTable;