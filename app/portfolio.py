import pandas as pd
import chromadb
import uuid
import os
import shutil


class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        # Use path relative to current working directory
        vectorstore_path = os.path.join(os.getcwd(), 'vectorstore')
        
        # Initialize ChromaDB client for version 1.0+
        # Handle potential corruption or version incompatibility
        max_retries = 2
        for attempt in range(max_retries):
            try:
                self.chroma_client = chromadb.PersistentClient(path=vectorstore_path)
                # Test if client works by trying to access it
                _ = self.chroma_client.list_collections()
                break  # Success, exit retry loop
            except (ValueError, Exception) as e:
                # If initialization fails, remove corrupted/incompatible vectorstore
                if os.path.exists(vectorstore_path) and attempt < max_retries - 1:
                    try:
                        shutil.rmtree(vectorstore_path)
                    except Exception:
                        pass
                elif attempt == max_retries - 1:
                    # Last attempt failed, raise the error
                    raise ValueError(
                        f"Failed to initialize ChromaDB after {max_retries} attempts. "
                        f"Please manually delete the 'vectorstore' directory and try again."
                    ) from e
        
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        # Handle both single skill (string) and multiple skills (list)
        if isinstance(skills, str):
            skills = [skills]
        elif not skills or len(skills) == 0:
            return "No relevant portfolio links found"
        
        # Query all skills at once (more efficient)
        results = self.collection.query(query_texts=skills, n_results=2)
        metadatas = results.get('metadatas', [])
        
        # Collect unique links from all results
        all_links = []
        seen_links = set()
        
        # ChromaDB returns a list where each element corresponds to results for each query text
        for metadata_list in metadatas:
            if isinstance(metadata_list, list):
                # Each element in metadata_list is a dict with 'links' key
                for metadata in metadata_list:
                    if isinstance(metadata, dict):
                        link = metadata.get('links', '')
                        if link and link not in seen_links:
                            all_links.append(link)
                            seen_links.add(link)
            elif isinstance(metadata_list, dict):
                # Direct dict format
                link = metadata_list.get('links', '')
                if link and link not in seen_links:
                    all_links.append(link)
                    seen_links.add(link)
        
        # Return as a formatted string for the LLM
        if all_links:
            return ', '.join(all_links)
        return "No relevant portfolio links found"
