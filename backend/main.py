from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil
import zipfile
from io import BytesIO
from pathlib import Path

from embeddings import extract_embedding
from clustering import run_clustering
from database import init_db, add_image, update_clusters, get_all_images, clear_database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

init_db()

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """Upload an image and extract its features"""
    try:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"🔄 Extracting embedding for {file_path}")
        
        embedding = extract_embedding(str(file_path))
        
        import numpy as np
        if not isinstance(embedding, np.ndarray):
            raise ValueError(f"Embedding must be numpy array, got {type(embedding)}")
        
        print(f"✅ Embedding shape: {embedding.shape}, type: {type(embedding)}")
        
        add_image(file.filename, embedding)
        
        all_images = get_all_images()
        print(f"✅ Finished embedding for {file_path}")
        print(f"📦 Total embeddings: {len(all_images)}")
        
        return JSONResponse({
            "message": "Image uploaded successfully",
            "filename": file.filename,
            "total_images": len(all_images),
            "embedding_shape": embedding.shape[0]
        })
    
    except Exception as e:
        print(f"❌ Error uploading image: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cluster")
async def cluster_images(eps: float = 0.25, min_samples: int = 2):
    """Perform clustering on uploaded images using DBSCAN"""
    try:
        images = get_all_images()
        
        if len(images) == 0:
            raise HTTPException(status_code=400, detail="No images uploaded yet")
        
        if len(images) < 2:
            raise HTTPException(status_code=400, detail="Need at least 2 images for clustering")
        
        print(f"🔄 Starting DBSCAN clustering on {len(images)} images")
        print(f"📊 Parameters: eps={eps}, min_samples={min_samples}")
        
        embeddings = [img['embedding'] for img in images]
        cluster_labels = run_clustering(embeddings, eps=eps, min_samples=min_samples)
        
        print(f"📊 Clustering results: {cluster_labels}")
        
        clustered = {}
        noise_images = []
        
        for idx, label in enumerate(cluster_labels):
            label = int(label)
            
            image_data = {
                'id': images[idx]['id'],
                'filename': images[idx]['filename'],
                'url': f"/uploads/{images[idx]['filename']}"
            }
            
            if label == -1:
                noise_images.append(image_data)
                continue
                
            if label not in clustered:
                clustered[label] = []
            
            clustered[label].append(image_data)
        
        update_clusters(clustered)
        
        print(f"✅ Clustering completed successfully")
        print(f"   - Found {len(clustered)} clusters")
        print(f"   - {len(noise_images)} noise points")
        
        return JSONResponse({
            "message": "Clustering completed successfully",
            "clusters": clustered,
            "num_clusters": len(clustered),
            "noise_images": noise_images,
            "parameters": {"eps": eps, "min_samples": min_samples},
            "tip": "Try adjusting eps: lower (0.15-0.20) for more clusters, higher (0.30-0.40) for fewer clusters"
        })
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Clustering error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cluster/stats/{cluster_id}")
async def get_cluster_stats(cluster_id: int):
    """Get statistics for a specific cluster"""
    try:
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
        
        images = get_all_images()
        cluster_images = [img for img in images if img['cluster_id'] == cluster_id]
        
        if not cluster_images:
            raise HTTPException(status_code=404, detail="Cluster not found")
        
        if len(cluster_images) < 2:
            return {
                "cluster_id": cluster_id,
                "num_images": 1,
                "avg_similarity": 1.0,
                "coherence": "perfect",
                "similarity_percent": 100.0
            }
        
        embeddings = np.array([img['embedding'] for img in cluster_images])
        similarities = cosine_similarity(embeddings)
        upper_triangle = similarities[np.triu_indices_from(similarities, k=1)]
        avg_similarity = float(np.mean(upper_triangle))
        
        if avg_similarity >= 0.85:
            coherence = "excellent"
        elif avg_similarity >= 0.75:
            coherence = "good"
        elif avg_similarity >= 0.65:
            coherence = "moderate"
        else:
            coherence = "loose"
        
        return {
            "cluster_id": cluster_id,
            "num_images": len(cluster_images),
            "avg_similarity": round(avg_similarity, 3),
            "coherence": coherence,
            "similarity_percent": round(avg_similarity * 100, 1)
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/cluster/{cluster_id}")
async def download_cluster(cluster_id: int):
    """Download all images in a cluster as ZIP"""
    try:
        images = get_all_images()
        cluster_images = [img for img in images if img['cluster_id'] == cluster_id]
        
        if not cluster_images:
            raise HTTPException(status_code=404, detail="Cluster not found")
        
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for img in cluster_images:
                file_path = UPLOAD_DIR / img['filename']
                if file_path.exists():
                    zip_file.write(file_path, img['filename'])
        
        zip_buffer.seek(0)
        
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename=group_{cluster_id + 1}.zip"}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Download error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/images")
async def get_images():
    """Get all uploaded images"""
    try:
        images = get_all_images()
        
        result = []
        for img in images:
            result.append({
                'id': img['id'],
                'filename': img['filename'],
                'url': f"/uploads/{img['filename']}",
                'cluster_id': img['cluster_id']
            })
        
        return JSONResponse({
            "images": result,
            "total": len(result)
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/clear")
async def clear_all():
    """Clear all uploaded images and database"""
    try:
        clear_database()
        
        for file in UPLOAD_DIR.glob("*"):
            if file.is_file():
                file.unlink()
        
        return JSONResponse({
            "message": "All data cleared successfully"
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Visual Clustering API - DINOv2 + DBSCAN",
        "version": "3.0",
        "endpoints": {
            "POST /upload": "Upload an image",
            "GET /cluster": "Cluster images (params: eps, min_samples)",
            "GET /cluster/stats/{id}": "Get cluster statistics",
            "GET /download/cluster/{id}": "Download cluster as ZIP",
            "GET /images": "Get all images",
            "DELETE /clear": "Clear all data"
        },
        "clustering_tips": {
            "strict_separation": "Use eps=0.20 to separate dogs, cats, humans, cars",
            "moderate_grouping": "Use eps=0.25 for balanced clustering (default)",
            "loose_grouping": "Use eps=0.35 for broader categories"
        }
    }


try:
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
except Exception as e:
    print(f"Note: Could not mount uploads directory: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)