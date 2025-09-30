// frontend/src/App.js
import React, { useState, useEffect } from "react";
import { supabase } from "./supabaseClient";
import "./App.css";
import ImageUpload from "./ImageUpload";
import VirtualTryOn from "./VirtualTryOn"; // 1. Importar o novo componente

function App() {
  const [session, setSession] = useState(null);
  const [bodyPhotoUrl, setBodyPhotoUrl] = useState(''); // 2. Gerenciar o estado da URL

  useEffect(() => {
    // Restaurar sessão
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      if (session) {
        // Se há sessão, buscar a foto do perfil
        getProfile(session);
      }
    });

    // Ouvir mudanças na autenticação
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      if (session) {
        getProfile(session);
      } else {
        setBodyPhotoUrl(''); // Limpar a foto ao fazer logout
      }
    });

    return () => subscription.unsubscribe();
  }, []);

  const getProfile = async (currentSession) => {
    try {
      const { user } = currentSession;
      let { data, error, status } = await supabase
        .from("usuarios")
        .select(`body_photo_url`)
        .eq("id", user.id)
        .single();

      if (error && status !== 406) throw error;

      if (data) {
        setBodyPhotoUrl(data.body_photo_url);
      }
    } catch (error) {
      console.error("Erro ao buscar perfil:", error.message);
    }
  };

  const handleGoogleLogin = async () => {
    const { error } = await supabase.auth.signInWithOAuth({ provider: "google" });
    if (error) console.error("Error logging in with Google:", error.message);
  };

  const handleLogout = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) console.error("Error logging out:", error.message);
  };

  // 4. Handler para o sucesso do upload
  const handleUploadSuccess = (url) => {
    setBodyPhotoUrl(url);
  };

  const handleChangePhoto = () => {
    setBodyPhotoUrl(''); // Limpa a URL, fazendo o ImageUpload aparecer
  };

  return (
    <div className="App">
      <main className="App-main">
        {!session ? (
          <div className="auth-container">
            <h1>Provador Virtual</h1>
            <p>Sua experiência de compra, reinventada.</p>
            <button onClick={handleGoogleLogin} className="login-button">
              Login com Google
            </button>
          </div>
        ) : (
          <div className="content-container">
            <div className="user-header">
              <span>Olá, {session.user.email}</span>
              <button onClick={handleLogout} className="logout-button">Sair</button>
            </div>

            {/* 3. Renderização condicional */}
            {!bodyPhotoUrl ? (
              <ImageUpload session={session} onUploadSuccess={handleUploadSuccess} />
            ) : (
              <VirtualTryOn 
                session={session} 
                bodyPhotoUrl={bodyPhotoUrl} 
                onChangePhoto={handleChangePhoto} // Passando a função aqui
              />
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
