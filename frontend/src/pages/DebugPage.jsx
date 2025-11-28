import { useState, useEffect } from 'react';

export default function DebugPage() {
  const [info, setInfo] = useState({});

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const refresh = localStorage.getItem('refresh_token');
    const user = localStorage.getItem('user');
    
    setInfo({
      hasToken: !!token,
      tokenLength: token?.length || 0,
      tokenPreview: token?.substring(0, 20) + '...',
      hasRefresh: !!refresh,
      user: user ? JSON.parse(user) : null
    });

    // Test API call
    if (token) {
      fetch('http://localhost:8000/api/v1/auth/devices/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      .then(res => {
        console.log('API Response Status:', res.status);
        return res.json();
      })
      .then(data => {
        console.log('API Response Data:', data);
        setInfo(prev => ({ ...prev, apiResponse: data, apiStatus: 'success' }));
      })
      .catch(err => {
        console.error('API Error:', err);
        setInfo(prev => ({ ...prev, apiError: err.message, apiStatus: 'error' }));
      });
    }
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h1>🐛 Debug Info</h1>
      
      <div style={{ background: '#f5f5f5', padding: '15px', marginBottom: '10px', borderRadius: '5px' }}>
        <h3>localStorage:</h3>
        <pre>{JSON.stringify(info, null, 2)}</pre>
      </div>

      <div style={{ background: '#fff3cd', padding: '15px', borderRadius: '5px' }}>
        <h3>Browser Console:</h3>
        <p>Mở Developer Tools (F12) và xem Console tab để xem API logs</p>
      </div>
    </div>
  );
}
