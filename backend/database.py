import sqlite3
import json
import numpy as np

DB_PATH = "clustering.db"

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Images table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            embedding TEXT NOT NULL,
            cluster_id INTEGER
        )
    """)
    
    # Clusters table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clusters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cluster_number INTEGER NOT NULL,
            image_ids TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def add_image(filename: str, embedding: np.ndarray):
    """Add an image with its embedding to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Convert numpy array to JSON string for storage
    embedding_json = json.dumps(embedding.tolist())
    
    cursor.execute(
        "INSERT INTO images (filename, embedding, cluster_id) VALUES (?, ?, NULL)",
        (filename, embedding_json)
    )
    
    conn.commit()
    conn.close()

def update_clusters(clustered_data):
    """Update the database with cluster assignments"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Reset all cluster assignments first
    cursor.execute("UPDATE images SET cluster_id = NULL")
    cursor.execute("DELETE FROM clusters")
    
    # Update each image with its cluster assignment
    for cluster_id, images in clustered_data.items():
        # Save cluster info
        image_ids_json = json.dumps([img['id'] for img in images])
        cursor.execute(
            "INSERT INTO clusters (cluster_number, image_ids) VALUES (?, ?)",
            (int(cluster_id), image_ids_json)
        )
        
        # Update each image's cluster_id
        for img in images:
            cursor.execute(
                "UPDATE images SET cluster_id = ? WHERE id = ?",
                (int(cluster_id), img['id'])
            )
    
    conn.commit()
    conn.close()
    print(f"✅ Updated {len(clustered_data)} clusters in database")

def get_all_images():
    """Retrieve all images with their embeddings"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, filename, embedding, cluster_id FROM images")
    rows = cursor.fetchall()
    
    conn.close()
    
    images = []
    for row in rows:
        images.append({
            'id': row[0],
            'filename': row[1],
            'embedding': np.array(json.loads(row[2])),
            'cluster_id': row[3]
        })
    
    return images

def get_clusters():
    """Retrieve all clusters with their images"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT cluster_number, image_ids FROM clusters")
    rows = cursor.fetchall()
    
    conn.close()
    
    clusters = {}
    for row in rows:
        cluster_num = row[0]
        image_ids = json.loads(row[1])
        clusters[cluster_num] = image_ids
    
    return clusters

def clear_database():
    """Clear all data from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM images")
    cursor.execute("DELETE FROM clusters")
    
    conn.commit()
    conn.close()

# Initialize database on import
init_db()