import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline, Box, Typography } from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import theme from './theme';
import PMDashboard from './pages/PM/PMDashboard';
import PMTasks from './pages/PM/PMTasks';
import Login from './pages/Auth/Login';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import MainLayout from './layouts/MainLayout';

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
        <AuthProvider>
          <BrowserRouter>
            <Routes>
              {/* Public Routes */}
              <Route path="/login" element={<Login />} />
              
              {/* Protected Routes */}
              <Route path="/" element={
                <ProtectedRoute>
                  <MainLayout />
                </ProtectedRoute>
              }>
                <Route index element={
                  <Box sx={{ p: 4 }}>
                    <Typography variant="h4" gutterBottom>
                      SLDC Operational Copilot
                    </Typography>
                    <Typography variant="body1" color="text.secondary">
                      System running. Use the navigation to access specific modules.
                    </Typography>
                  </Box>
                } />
                <Route path="pm" element={<PMDashboard />} />
                <Route path="pm/tasks" element={<PMTasks />} />
              </Route>
            </Routes>
          </BrowserRouter>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
