import React from 'react';

function ImageViewer({ imageUrl, metadata, isLoading }) {
  const handleExport = () => {
    if (imageUrl) {
      const link = document.createElement('a');
      link.href = imageUrl;
      link.download = imageUrl.split('/').pop() || 'processed-image.png';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <div className="module">
      <h2>3. Visualize & Export (P0.3)</h2>
      <div className="image-container">
        {isLoading && <p>Loading image...</p>}
        {imageUrl && !isLoading && <img src={imageUrl} alt="Processed astronomical" />}
        {!imageUrl && !isLoading && <p>Your colorized image will appear here.</p>}
      </div>
      {imageUrl && <button onClick={handleExport}>Export Image (PNG)</button>}
      {metadata && (
        <div className="metadata-container">
          <h3>FITS Metadata Display</h3>
          <pre>{JSON.stringify(Object.fromEntries(Object.entries(metadata).slice(0, 15)), null, 2)}</pre>
          <p>...and more</p>
        </div>
      )}
    </div>
  );
}

export default ImageViewer;