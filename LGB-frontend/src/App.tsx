import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { ThemeProvider, CssBaseline, Box, Typography, AppBar, Toolbar, Button } from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import theme from './theme';
import PMDashboard from './modules/pm/Dashboard';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      staleTime: 1000 * 60, // 1 minute stale time default
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <BrowserRouter>
          <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
            <AppBar position="static" color="transparent" elevation={0} sx={{ borderBottom: '1px solid #333' }}>
              <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1, color: 'primary.main' }}>
                  SLDC Copilot
                </Typography>
                <Button color="inherit" component={Link} to="/">Home</Button>
                <Button color="inherit" component={Link} to="/pm">Project Tracker</Button>
              </Toolbar>
            </AppBar>
            
            <Box sx={{ p: 4, flexGrow: 1, overflow: 'auto' }}>
              <Routes>
                <Route path="/" element={
                  <Box>
                    <Typography variant="h4" gutterBottom>
                      SLDC Operational Copilot
                    </Typography>
                    <Typography variant="body1" color="text.secondary">
                      System running. Use the navigation to access specific modules.
                    </Typography>
                  </Box>
                } />
                <Route path="/pm" element={<PMDashboard />} />
              </Routes>
            </Box>
          </Box>
        </BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
