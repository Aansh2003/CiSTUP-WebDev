import React, { useState } from 'react';
import './App.css';

function SensorDemo() {
    const [status, setStatus] = useState('');
    const [imageSrc, setImageSrc] = useState(null);

    const handleImageUpload = async (event) => {
        const file = event.target.files[0];
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://127.0.0.1:5000/upload', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data);
                setStatus('File uploaded successfully: ' + data.filename);
                setImageSrc("http://127.0.0.1:5000/image"); // Display the uploaded image
            } else {
                setStatus('Failed to upload file');
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            setStatus('Failed to upload file');
        }
    };

    const handleButtonClick = (endpoint) => {
        fetch('http://127.0.0.1:5000' + endpoint, { method: 'POST' })
            .then(response => response.json())
            .then(data => setStatus('Variable toggled: ' + data.toggle_variable))
            .catch(error => console.error(error));
    };

    return (
        <div>
            <h1>
                <span>&nbsp;Image processing</span>
            </h1>

            <div>
                <div className="title">
                    <h2>Image Preview</h2>
                </div>
                <div className="box">
                    <div style={{ width: '40%', height: '500px' }}>
                        {imageSrc ? (
                            <img src={imageSrc} alt="Uploaded Image" />
                        ) : (
                            <div class="file-upload">
                                <label for="upload" class="file-upload-label">Choose File</label>
                                <input type="file" id="upload" name="upload" onChange={handleImageUpload}></input>
                                <div class="file-name" id="file-name"></div>
                            </div>
                        )}
                    </div>
                    <div style={{ width: '60%', height: '500px' }}>
                        <div className="grid-container">
                            <button onClick={() => handleButtonClick('/model1')} id="model1">Yolo Model 1</button>
                            <button onClick={() => handleButtonClick('/model2')} id="model2">Convert BGR to RGB</button>
                            <button onClick={() => handleButtonClick('/bw')} id="bw">Black and white</button>
                            <button onClick={() => handleButtonClick('/sharp')} id="sharp">Sharpen</button>
                            <button onClick={() => handleButtonClick('/pause')} id="pause">Contours</button>
                            <button onClick={() => handleButtonClick('/fr')} id="fr">Increase red intensity</button>
                        </div>
                    </div>
                </div>
            </div>

            <div id="status">{status}</div>
        </div>
    );
}

export default SensorDemo;
