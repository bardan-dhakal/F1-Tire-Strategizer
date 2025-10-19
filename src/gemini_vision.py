import os
import json
import base64
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_tire_with_gemini(image_path):
    prompt = """You are an F1 tire expert. Analyze this tire image and extract these features in JSON format.

Return ONLY valid JSON, no other text.

{
  "color": "Matte black/Glossy black/purple tin/Grey-black/Pale grey",
  "compound": "soft/medium/hard/intermediate/wet",
  "wear_pattern": "uneven/inner/outer/center/even",
  "sidewall_deformation": true/false,
  "is_graining": true/false
}

IMPORTANT RULES:
- Only include categories that can be determined from the image
- DO NOT include: tyre_pressure, tyre_temperature, track_temperature (these cannot be seen in images)
- Skip compound if you cannot clearly see tire markings
- Use exact values from the options provided above
- If you can't determine something clearly, use these defaults:
  * color: "Matte black"
  * wear_pattern: "even" 
  * sidewall_deformation: false
  * is_graining: false

Guidelines:
- color: Look at the tire surface color (Matte black/Glossy black/purple tin/Grey-black/Pale grey)
- compound: Only if you can see clear tire markings (red=soft, yellow=medium, white=hard, green=intermediate, blue=wet)
- wear_pattern: 
  * "even" = uniform wear across tire
  * "inner" = more wear on inside edge
  * "outer" = more wear on outside edge  
  * "center" = more wear in middle
  * "uneven" = irregular/patchy wear
- sidewall_deformation: Is the sidewall bulging or collapsed? (true/false)
- is_graining: Is the surface rough with rubber particles? (true/false)"""
    image_data = encode_image_to_base64(image_path)
    
    response = model.generate_content([
        prompt,
        {
            "mime_type": "image/jpeg",
            "data": image_data
        }
    ])
    
    json_text = response.text.strip()
    if json_text.startswith('```json'):
        json_text = json_text[7:]
    if json_text.endswith('```'):
        json_text = json_text[:-3]
    
    return json.loads(json_text)
    

def process_tire_images():
    tire_images_dir = Path("tire_images")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    for lap_dir in tire_images_dir.iterdir():
        if lap_dir.is_dir() and lap_dir.name.startswith("lap_"):
            print(f"Processing {lap_dir.name}")
            output_file = f"{lap_dir.name}.json"
            output_path = output_dir / output_file
            
            if output_path.exists():
                print(f"Skipping: {output_path} - Output file already exists")
                continue
            
            for image_file in lap_dir.iterdir():
                analysis_result = analyze_tire_with_gemini(image_file)
                
                with open(output_path, 'w') as f:
                    json.dump(analysis_result, f, indent=2)
                print(f"Saved analysis to {output_path}")
                break

if __name__ == "__main__":
    process_tire_images()
