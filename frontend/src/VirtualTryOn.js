import React, { useState } from 'react';
import { supabase } from './supabaseClient';
import './VirtualTryOn.css';

// Ícone simples de upload como um componente React
const UploadIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="upload-icon">
        <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
    </svg>
);

const VirtualTryOn = ({ session, bodyPhotoUrl, onChangePhoto }) => {
    const [garmentFile, setGarmentFile] = useState(null);
    const [garmentPreview, setGarmentPreview] = useState(null);
    const [resultUrl, setResultUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleGarmentChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            setGarmentFile(file);
            const reader = new FileReader();
            reader.onloadend = () => {
                setGarmentPreview(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleTryOn = async () => {
        if (!garmentFile) {
            setError('Por favor, carregue uma imagem da roupa.');
            return;
        }

        setLoading(true);
        setError('');
        setResultUrl('');

        try {
            // 1. Upload da imagem da roupa para o Supabase Storage
            const fileExt = garmentFile.name.split('.').pop();
            const fileName = `${session.user.id}-${Date.now()}.${fileExt}`;
            const filePath = `${fileName}`;

            const { error: uploadError } = await supabase.storage
                .from('garment_photos') // NOVO BUCKET
                .upload(filePath, garmentFile);

            if (uploadError) throw uploadError;

            // 2. Obter a URL pública da imagem da roupa
            const { data: publicUrlData } = supabase.storage
                .from('garment_photos')
                .getPublicUrl(filePath);

            if (!publicUrlData.publicUrl) throw new Error('Não foi possível obter a URL pública da roupa.');

            const garmentImageUrl = publicUrlData.publicUrl;

            // 3. Chamar a API do backend
            const response = await fetch('http://localhost:8000/api/tryon', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${session.access_token}`,
                },
                body: JSON.stringify({
                    body_image_url: bodyPhotoUrl,
                    garment_image_url: garmentImageUrl,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Falha na chamada da API.');
            }

            // 4. Exibir o resultado (mockado por enquanto)
            setResultUrl(data.processed_image_url);

        } catch (err) {
            setError(err.message || 'Ocorreu um erro.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="tryon-container">
            <div className="tryon-header">
                <h2>Provador Virtual</h2>
            </div>

            <div className="image-display-grid">
                <div className="image-card" onClick={onChangePhoto} style={{ cursor: 'pointer' }}>
                    {bodyPhotoUrl ? <img src={bodyPhotoUrl} alt="Sua foto" /> : <div className="placeholder-text">Sua Foto</div>}
                </div>
                <div className="image-card">
                    <label htmlFor="garment-upload" style={{cursor: 'pointer'}}>
                        {garmentPreview ? <img src={garmentPreview} alt="Roupa" /> : <><UploadIcon /><div className='placeholder-text'>Foto da Roupa</div></>}
                    </label>
                    <input type="file" id="garment-upload" accept="image/*" onChange={handleGarmentChange} style={{ display: 'none' }} />
                </div>
                
                {resultUrl && (
                    <div className="image-card result-card">
                        <img src={resultUrl} alt="Resultado" />
                    </div>
                )}
            </div>

            {loading && <div className="loading-spinner"></div>}

            {error && <p style={{ color: 'red' }}>{error}</p>}

            <div className="tryon-controls">
                <button onClick={handleTryOn} className="tryon-button" disabled={loading || !garmentFile}>
                    {loading ? 'Processando...' : 'Ver como fica em mim'}
                </button>
            </div>
        </div>
    );
};

export default VirtualTryOn;
