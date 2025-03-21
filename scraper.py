import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from twocaptcha import TwoCaptcha  # Importing the 2Captcha service
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
import logging
import tldextract
import whois
from sentence_transformers import SentenceTransformer
import cv2
import numpy as np
import pandas as pd
import re
import face_recognition
import zipfile
import os

# Configure proxies
proxies = {
    "http": "http://your_proxy_here",
    "https": "http://your_proxy_here",
}

# Initialize 2Captcha
solver = TwoCaptcha('YOUR_API_KEY')  # Replace with your 2Captcha API key
model = SentenceTransformer('all-MiniLM-L6-v2')

def perform_search(target_name, first_name=None, last_name=None, location=None):
    """Perform a Google search using SerpAPI."""
    # Replace with your SerpAPI key and endpoint
    serpapi_key = 'YOUR_SERPAPI_KEY'
    search_url = f"https://serpapi.com/search.json?engine=google&q={target_name}&location={location}&api_key={serpapi_key}"
    
    response = requests.get(search_url)
    if response.status_code == 200:
        return response.json().get('organic_results', [])
    else:
        logging.error(f"Error fetching search results: {response.status_code}")
        return []

def scrape_data(target_name, first_name=None, last_name=None, location=None, reference_pictures=None):
    results = perform_search(target_name, first_name, last_name, location)
    detailed_results = []
    
    for result in results:
        link = result.get('link')
        if link:
            detailed_results.extend(explore_url(link, target_name, first_name, last_name, reference_pictures))
    
    # Sort and rank the data based on relevance
    ranked_results = rank_data(detailed_results, target_name, first_name, last_name)
    
    return ranked_results

def explore_url(url, target_name, first_name, last_name, reference_pictures):
    detailed_data = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        text_data = soup.get_text()
        if (first_name in text_data or last_name in text_data) and target_name in text_data:
            detailed_data.append({
                'url': url,
                'text': text_data
            })
        
        # Extract domain and metadata
        domain_info = extract_domain_info(url)
        detailed_data.append({'domain_info': domain_info})
        
        # Extract images and videos
        media_links = extract_media(soup)
        detailed_data.extend(media_links)
        
        # Compare with reference pictures if provided
        if reference_pictures:
            for media in media_links:
                if media['type'] == 'image':
                    check_image_similarity(media['url'], reference_pictures)
        
        return detailed_data
    
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while exploring URL {url}: {e}")
        return []

def extract_domain_info(url):
    """Extract domain and metadata from the URL."""
    extracted = tldextract.extract(url)
    domain = f"{extracted.domain}.{extracted.suffix}"
    metadata = whois.whois(domain)
    return {
        'domain': domain,
        'subdomain': extracted.subdomain,
        'metadata': metadata
    }

def extract_media(soup):
    """Extract images and videos from the BeautifulSoup object."""
    media_links = []
    
    # Extract images
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url:
            media_links.append({'type': 'image', 'url': img_url})
    
    # Extract videos (if any)
    for video in soup.find_all('video'):
        video_url = video.get('src')
        if video_url:
            media_links.append({'type': 'video', 'url': video_url})
            download_video(video_url)  # Download the video
    
    return media_links

def download_video(video_url):
    """Download a video using pytube."""
    try:
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path='downloads')  # Specify download directory
        logging.info(f"Downloaded video: {video_url}")
    except Exception as e:
        logging.error(f"Error downloading video: {e}")

def check_image_similarity(image_url, reference_pictures):
    """Check similarity of the image with reference pictures."""
    # Load the reference images
    reference_encodings = []
    for ref in reference_pictures:
        ref_image = face_recognition.load_image_file(ref)
        ref_encoding = face_recognition.face_encodings(ref_image)[0]
        reference_encodings.append(ref_encoding)

    # Load the image to check
    image = face_recognition.load_image_file(image_url)
    image_encoding = face_recognition.face_encodings(image)[0]

    # Compare with reference encodings
    matches = face_recognition.compare_faces(reference_encodings, image_encoding)
    if True in matches:
        logging.info(f"Image {image_url} matches with reference pictures.")

def rank_data(detailed_results, target_name, first_name, last_name):
    """Rank the extracted data based on relevance."""
    ranked_results = []
    for data in detailed_results:
        score = 0
        if target_name in data.get('text', ''):
            score += 1
        if first_name in data.get('text', '') or last_name in data.get('text', ''):
            score += 1
        # Add more scoring logic based on domain relevance or other criteria
        ranked_results.append((data, score))
    
    # Sort by score in descending order
    ranked_results.sort(key=lambda x: x[1], reverse=True)
    return [item[0] for item in ranked_results]

def extract_features_from_text(text):
    """Extract features from text using SentenceTransformer."""
    return model.encode(text)

def extract_features_from_image(image_path):
    """Extract features from an image using OpenCV."""
    image = cv2.imread(image_path)
    # Implement feature extraction logic here
    return image.flatten()  # Placeholder for actual feature extraction

def extract_frames(video_path):
    """Extract frames from a video."""
    video_capture = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        frames.append(frame)
    video_capture.release()
    return frames

def analyze_video(video_path):
    """Analyze a video for faces and features."""
    frames = extract_frames(video_path)
    for frame in frames:
        # Convert frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        # Process each face found
        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_image = rgb_frame[top:bottom, left:right]
            # Further processing can be done here (e.g., feature extraction)
            # Example: features = extract_features_from_image(face_image)

def reverse_image_search(reference_pictures):
    return []

def cluster_data(data):
    """Cluster data using DBSCAN."""
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data)
    clustering = DBSCAN(eps=0.5, min_samples=5).fit(X)
    return clustering.labels_

if __name__ == "__main__":
    target_name = input("Enter the target's name: ")
    first_name = input("Enter the first name (optional): ")
    last_name = input("Enter the last name (optional): ")
    location = input("Enter the location (optional): ")
    results = scrape_data(target_name, first_name, last_name, location)
    print(results)
    time.sleep(2)  # Rate limiting: wait for 2 seconds before the next request
