import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function GoogleLoginButton() {
  const { loginWithGoogle } = useAuth();
  const navigate = useNavigate();
  const [scriptLoaded, setScriptLoaded] = useState(false);

  const handleGoogleResponse = async (response) => {
    const result = await loginWithGoogle(response.credential);
    
    if (result.success) {
      navigate('/my-devices');
    } else {
      alert('Google login failed: ' + result.error);
    }
  };

  useEffect(() => {
    // Check if GOOGLE_CLIENT_ID is set
    const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
    if (!clientId || clientId === 'your-google-client-id.apps.googleusercontent.com') {
      console.warn('Google Client ID not configured');
      return;
    }

    // Load Google Sign-In script
    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;
    script.onload = () => {
      setScriptLoaded(true);
    };
    document.body.appendChild(script);

    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, []);

  useEffect(() => {
    if (scriptLoaded && window.google) {
      const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
      
      try {
        window.google.accounts.id.initialize({
          client_id: clientId,
          callback: handleGoogleResponse,
        });

        const buttonDiv = document.getElementById('google-signin-button');
        if (buttonDiv) {
          window.google.accounts.id.renderButton(buttonDiv, {
            theme: 'outline',
            size: 'large',
            text: 'signin_with',
            shape: 'rectangular',
            width: buttonDiv.offsetWidth || 300,
          });
        }
      } catch (error) {
        console.error('Google Sign-In initialization error:', error);
      }
    }
  }, [scriptLoaded]);

  // Show placeholder if client ID not configured
  const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
  if (!clientId || clientId === 'your-google-client-id.apps.googleusercontent.com') {
    return (
      <div className="w-full p-4 text-center bg-gray-100 rounded-lg text-gray-600 text-sm">
        ⚙️ Google OAuth chưa được cấu hình. <br/>
        Vui lòng cập nhật VITE_GOOGLE_CLIENT_ID trong frontend/.env
      </div>
    );
  }

  return (
    <div className="w-full">
      <div id="google-signin-button" className="w-full flex justify-center"></div>
    </div>
  );
}
