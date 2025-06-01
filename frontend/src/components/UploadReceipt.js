import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import {
  Box,
  Paper,
  Typography,
  Button,
  CircularProgress,
  Alert,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function UploadReceipt() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const onDrop = async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      // Upload file
      const formData = new FormData();
      formData.append('file', file);
      const uploadResponse = await axios.post(`${API_URL}/upload`, formData);
      const fileId = uploadResponse.data.id;

      // Validate file
      const validateResponse = await axios.post(`${API_URL}/validate/${fileId}`);
      if (!validateResponse.data.is_valid) {
        throw new Error(validateResponse.data.message);
      }

      // Process receipt
      const processResponse = await axios.post(`${API_URL}/process/${fileId}`);
      if (!processResponse.data.success) {
        throw new Error('Failed to process receipt');
      }

      setSuccess(true);
      setTimeout(() => {
        navigate(`/receipts/${processResponse.data.receipt_id}`);
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    multiple: false,
  });

  return (
    <Box sx={{ maxWidth: 600, mx: 'auto', mt: 4 }}>
      <Paper
        sx={{
          p: 4,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Typography variant="h5" gutterBottom>
          Upload Receipt
        </Typography>

        {error && (
          <Alert severity="error" sx={{ width: '100%', mb: 2 }}>
            {error}
          </Alert>
        )}

        {success && (
          <Alert severity="success" sx={{ width: '100%', mb: 2 }}>
            Receipt processed successfully! Redirecting...
          </Alert>
        )}

        <Box
          {...getRootProps()}
          sx={{
            border: '2px dashed #ccc',
            borderRadius: 2,
            p: 4,
            width: '100%',
            textAlign: 'center',
            cursor: 'pointer',
            '&:hover': {
              borderColor: 'primary.main',
            },
          }}
        >
          <input {...getInputProps()} />
          {loading ? (
            <CircularProgress />
          ) : (
            <>
              <CloudUploadIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
              <Typography>
                {isDragActive
                  ? 'Drop the PDF receipt here'
                  : 'Drag and drop a PDF receipt here, or click to select'}
              </Typography>
            </>
          )}
        </Box>

        <Button
          variant="contained"
          color="primary"
          sx={{ mt: 2 }}
          onClick={() => navigate('/')}
        >
          View All Receipts
        </Button>
      </Paper>
    </Box>
  );
}

export default UploadReceipt; 