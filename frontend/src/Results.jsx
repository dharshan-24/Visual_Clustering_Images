 import React, { useState, useEffect } from 'react';
import './Results.css';

const Results = () => {
  const [clusters, setClusters] = useState({});
  const [clusterStats, setClusterStats] = useState({});
  const [loading, setLoading] = useState(false);
  const [epsValue, setEpsValue] = useState(0.25);
  const [totalImages, setTotalImages] = useState(0);
  const [selectedImage, setSelectedImage] = useState(null);
  const [toast, setToast] = useState({ show: false, message: '', type: 'success' });

  const API_URL = 'http://127.0.0.1:8000';

  // Color palette for different groups
  const groupColors = [
    { bg: 'rgba(16, 185, 129, 0.1)', border: '#10b981', glow: 'rgba(16, 185, 129, 0.3)' }, // Green
    { bg: 'rgba(59, 130, 246, 0.1)', border: '#3b82f6', glow: 'rgba(59, 130, 246, 0.3)' }, // Blue
    { bg: 'rgba(168, 85, 247, 0.1)', border: '#a855f7', glow: 'rgba(168, 85, 247, 0.3)' }, // Purple
    { bg: 'rgba(239, 68, 68, 0.1)', border: '#ef4444', glow: 'rgba(239, 68, 68, 0.3)' },   // Red
    { bg: 'rgba(245, 158, 11, 0.1)', border: '#f59e0b', glow: 'rgba(245, 158, 11, 0.3)' }, // Orange
    { bg: 'rgba(236, 72, 153, 0.1)', border: '#ec4899', glow: 'rgba(236, 72, 153, 0.3)' }, // Pink
    { bg: 'rgba(20, 184, 166, 0.1)', border: '#14b8a6', glow: 'rgba(20, 184, 166, 0.3)' }, // Teal
    { bg: 'rgba(251, 191, 36, 0.1)', border: '#fbbf24', glow: 'rgba(251, 191, 36, 0.3)' }  // Yellow
  ];

  useEffect(() => {
    fetchImages();
  }, []);

  useEffect(() => {
    if (toast.show) {
      const timer = setTimeout(() => {
        setToast({ ...toast, show: false });
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [toast.show]);

  const showToast = (message, type) => {
    setToast({ show: true, message, type });
  };

  const fetchImages = async () => {
    try {
      const response = await fetch(API_URL + '/images');
      const data = await response.json();
      setTotalImages(data.total);
      
      const groupedClusters = {};
      data.images.forEach(img => {
        if (img.cluster_id !== null && img.cluster_id !== undefined) {
          if (!groupedClusters[img.cluster_id]) {
            groupedClusters[img.cluster_id] = [];
          }
          groupedClusters[img.cluster_id].push(img);
        }
      });
      
      setClusters(groupedClusters);
      
      // Fetch stats for each cluster
      Object.keys(groupedClusters).forEach(clusterId => {
        fetchClusterStats(clusterId);
      });
    } catch (error) {
      console.error('Error fetching images:', error);
    }
  };

  const fetchClusterStats = async (clusterId) => {
    try {
      const response = await fetch(API_URL + '/cluster/stats/' + clusterId);
      const data = await response.json();
      setClusterStats(prev => ({ ...prev, [clusterId]: data }));
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const performClustering = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        API_URL + '/cluster?eps=' + epsValue + '&min_samples=2'
      );
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Clustering failed');
      }
      const data = await response.json();
      await fetchImages();
      showToast('✨ Found ' + data.num_clusters + ' clusters!', 'success');
    } catch (error) {
      console.error('Clustering error:', error);
      showToast('❌ ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const files = event.target.files;
    if (!files.length) return;
    setLoading(true);
    for (let file of files) {
      const formData = new FormData();
      formData.append('file', file);
      try {
        await fetch(API_URL + '/upload', { method: 'POST', body: formData });
      } catch (error) {
        console.error('Upload error:', error);
      }
    }
    await fetchImages();
    setLoading(false);
    showToast('✅ Uploaded ' + files.length + ' image(s)', 'success');
  };

  const clearAll = async () => {
    if (!window.confirm('Are you sure?')) return;
    try {
      await fetch(API_URL + '/clear', { method: 'DELETE' });
      setClusters({});
      setClusterStats({});
      setTotalImages(0);
      showToast('🗑️ All data cleared', 'success');
    } catch (error) {
      console.error('Clear error:', error);
    }
  };

  const downloadCluster = async (clusterId) => {
    try {
      showToast('⏳ Preparing download...', 'success');
      const response = await fetch(API_URL + '/download/cluster/' + clusterId);
      if (!response.ok) throw new Error('Download failed');
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'group_' + (parseInt(clusterId) + 1) + '.zip';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
      showToast('✅ Downloaded!', 'success');
    } catch (error) {
      showToast('❌ Download failed', 'error');
    }
  };

  const getSensitivityLabel = () => {
    if (epsValue <= 0.15) return 'Very Strict';
    if (epsValue <= 0.20) return 'Strict';
    if (epsValue <= 0.25) return 'Balanced';
    if (epsValue <= 0.30) return 'Loose';
    return 'Very Loose';
  };

  const getCoherenceIcon = (coherence) => {
    switch(coherence) {
      case 'excellent': return '⭐⭐⭐';
      case 'good': return '⭐⭐';
      case 'moderate': return '⭐';
      default: return '•';
    }
  };

  const clusterCount = Object.keys(clusters).length;

  return (
    <div className="results-container">
      {toast.show && (
        <div className={'toast toast-' + toast.type}>
          <span>{toast.message}</span>
        </div>
      )}

      <header className="results-header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">D</div>
            <div className="logo-text">
              <h1>DINOv2 Smart Grouping</h1>
              <span className="subtitle">Visual Clustering Dashboard</span>
            </div>
          </div>

          <div className="header-actions">
            <label className="btn btn-secondary">
              <input type="file" multiple accept="image/*" onChange={handleFileUpload} style={{ display: 'none' }} />
              Upload Images
            </label>

            <div className="slider-wrapper">
              <div className="slider-top">
                <span className="slider-title">Sensitivity</span>
                <span className="slider-number">{epsValue}</span>
              </div>
              <input type="range" min="0.10" max="0.40" step="0.05" value={epsValue}
                onChange={(e) => setEpsValue(parseFloat(e.target.value))} className="eps-slider" />
              <div className="slider-hint">
                <span>Strict</span>
                <span className="sensitivity-label">{getSensitivityLabel()}</span>
                <span>Loose</span>
              </div>
            </div>

            <button className="btn btn-primary" onClick={performClustering} disabled={loading || totalImages < 2}>
              Cluster Images
            </button>
            <button className="btn btn-danger" onClick={clearAll}>Clear All</button>
          </div>
        </div>
      </header>

      <div className="stats-bar">
        <div className="stat-card">
          <div className="stat-label">Total Images</div>
          <div className="stat-value">{totalImages}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Clusters Found</div>
          <div className="stat-value">{clusterCount}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Status</div>
          <div className="stat-value status-text">
            {loading ? 'Processing...' : clusterCount > 0 ? 'Clustered' : 'Ready'}
          </div>
        </div>
      </div>

      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <p>Processing with eps={epsValue}...</p>
        </div>
      )}

      <div className="clusters-section">
        {clusterCount === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🖼️</div>
            <h2>No clusters yet</h2>
            <p>Upload images and click Cluster Images to get started</p>
          </div>
        ) : (
          Object.keys(clusters).sort((a, b) => a - b).map((clusterId, index) => {
            const colorTheme = groupColors[index % groupColors.length];
            const stats = clusterStats[clusterId];
            
            return (
              <div key={clusterId} className="cluster-group"
                style={{
                  animationDelay: (index * 0.1) + 's',
                  background: colorTheme.bg,
                  borderColor: colorTheme.border
                }}>
                <div className="cluster-header">
                  <div className="cluster-title-section">
                    <h2 style={{ color: colorTheme.border }}>
                      Group {parseInt(clusterId) + 1}
                    </h2>
                    {stats && (
                      <div className="cluster-stats">
                        <span className="stat-item" title="Average Similarity">
                          📊 {stats.similarity_percent}%
                        </span>
                        <span className="stat-item" title="Coherence">
                          {getCoherenceIcon(stats.coherence)} {stats.coherence}
                        </span>
                      </div>
                    )}
                  </div>
                  <div className="cluster-header-right">
                    <span className="cluster-badge" style={{
                      background: colorTheme.border,
                      boxShadow: '0 0 20px ' + colorTheme.glow
                    }}>
                      {clusters[clusterId].length} Images
                    </span>
                    <button className="btn-download" onClick={() => downloadCluster(clusterId)}
                      style={{ borderColor: colorTheme.border, color: colorTheme.border }}>
                      📥 Download
                    </button>
                  </div>
                </div>

                <div className="cluster-grid">
                  {clusters[clusterId].map((image) => (
                    <div key={image.id} className="image-card"
                      onClick={() => setSelectedImage(API_URL + image.url)}
                      style={{ borderColor: colorTheme.border }}>
                      <div className="image-wrapper">
                        <img src={API_URL + image.url} alt={image.filename} loading="lazy" />
                      </div>
                      <div className="image-info">
                        <span className="image-filename">{image.filename}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })
        )}
      </div>

      {selectedImage && (
        <div className="modal" onClick={() => setSelectedImage(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setSelectedImage(null)}>✕</button>
            <img src={selectedImage} alt="Full size" />
          </div>
        </div>
      )}
    </div>
  );
};

export default Results;