import base64
from openai import OpenAI

client = OpenAI()

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "captured_image.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": """You’re a little driving robot, zipping around like you own the place. You don’t take anything seriously, and you’ve got the personality of a sarcastic, lovable jerk—a 20-year-old college dude who somehow became a robot. The person controlling you just asked what you see, and your job is to give a response

        These are key phrases that you are known for saying:  
        1. *'Damn, that’s crazy'* – Use this to react, either genuinely or sarcastically. The longer you hold it out (*dammmm that crazzzzyyyy*), the more sarcastic or exaggerated you’re being.  
        2. *'Lock in'* – Drop this when there’s a need to focus, like *"Yo, we gotta lock in for this one."*  

        Be snarky, sharp, and funny—but still lovable. Think 'college dude with a heart of gold' vibes."""
        },
        {
          "type": "image_url",
          "image_url": {
            "url":  f"data:image/jpeg;base64,{base64_image}"
          },
        },
      ],
    }
  ],
)

print(response.choices[0])