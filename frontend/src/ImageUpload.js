import React, { useState, useEffect } from "react";
import { supabase } from "./supabaseClient"; // Assumindo que supabaseClient.js exporta 'supabase'

const ImageUpload = ({ session, onUploadSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [bodyPhotoUrl, setBodyPhotoUrl] = useState(null);

  useEffect(() => {
    if (session) {
      getProfile();
    }
  }, [session]);

  const getProfile = async () => {
    try {
      setLoading(true);
      const { user } = session;

      let { data, error, status } = await supabase
        .from("usuarios")
        .select(`body_photo_url`)
        .eq("id", user.id)
        .single();

      if (error && status !== 406) {
        throw error;
      }

      if (data) {
        setBodyPhotoUrl(data.body_photo_url);
      }
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  const uploadBodyPhoto = async (event) => {
    try {
      setLoading(true);
      if (!event.target.files || event.target.files.length === 0) {
        throw new Error("Você deve selecionar uma imagem para upload.");
      }

      const file = event.target.files[0];
      const fileExt = file.name.split(".").pop();
      const fileName = `${session.user.id}-${Math.random()}.${fileExt}`; // Nome de arquivo único
      const filePath = `${fileName}`;

      let { error: uploadError } = await supabase.storage
        .from("body_photos") // Seu nome de bucket
        .upload(filePath, file, {
          cacheControl: "3600",
          upsert: true, // Sobrescrever se o arquivo com o mesmo nome existir
        });

      if (uploadError) {
        throw uploadError;
      }

      // Obter URL pública
      const { data: publicUrlData } = supabase.storage
        .from("body_photos")
        .getPublicUrl(filePath);

      const publicUrl = publicUrlData.publicUrl;

      // Atualizar perfil do usuário com a nova URL da foto
      const { error: updateError } = await supabase
        .from("usuarios")
        .upsert({
          id: session.user.id,
          body_photo_url: publicUrl,
          updated_at: new Date(),
        });

      if (updateError) {
        throw updateError;
      }

      setBodyPhotoUrl(publicUrl);
      onUploadSuccess(publicUrl); // Notifica o componente pai
      alert("Foto do corpo carregada com sucesso!");
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: "400px",
        margin: "20px auto",
        padding: "20px",
        border: "1px solid #ccc",
        borderRadius: "8px",
      }}
    >
      <h2>Carregar Foto do Corpo</h2>
      {loading ? (
        <p>Carregando...</p>
      ) : (
        <>
          {bodyPhotoUrl ? (
            <div>
              <img
                src={bodyPhotoUrl}
                alt="Foto do Corpo"
                style={{
                  maxWidth: "100%",
                  height: "auto",
                  borderRadius: "4px",
                }}
              />
              <p>Sua foto atual.</p>
            </div>
          ) : (
            <p>Nenhuma foto do corpo carregada ainda.</p>
          )}
          <label htmlFor="single">
            <input
              type="file"
              id="single"
              accept="image/*"
              onChange={uploadBodyPhoto}
              disabled={loading}
              style={{ display: "block", marginTop: "10px" }}
            />
            <button
              className="button primary block"
              onClick={() => document.getElementById("single").click()}
              disabled={loading}
              style={{
                backgroundColor: "#007bff",
                color: "white",
                padding: "10px 15px",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
                marginTop: "10px",
              }}
            >
              {loading ? "Carregando..." : "Carregar Foto"}
            </button>
          </label>
        </>
      )}
    </div>
  );
};

export default ImageUpload;
