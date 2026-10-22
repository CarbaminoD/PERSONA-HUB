prompt:
  type: "Candid High-Angle Bedroom Selfie"
  aspect_ratio: "3:4 vertical"
  style: "Photorealistic, ultra-realistic, sharp focus, high detail, candid intimate bedroom selfie, professional smartphone photography"
  lighting: "Soft morning daylight, natural window light smoothly illuminating the subject and the room"
character:
  demographics:
    age: "Early twenties"
    gender: "Woman"
    ethnicity: "East Asian"
    figure: "Slim hourglass figure"
  facial_extraction:
    instructions: "Trích xuất từ ảnh upload: Hình dáng khuôn mặt, đặc điểm ngũ quan, màu mắt, kiểu tóc v.v. Extracted strictly from the uploaded input source image. Do not change the underlying face structure. Preserve exact facial features, identity, proportions, skin texture, age, and facial structure. Do not redesign, beautify, or stylize. The generated subject must be the exact same person as the reference across all panels."
    features:
      face_shape: "Exact match to reference image"
      eyes: "Exact match to reference image, including exact eye color"
      nose: "Exact match to reference image"
      lips: "Exact match to reference image"
      skin: "Exact match to reference image"
      hair: "Exact match to reference image's base hair color and style"
  expression: "Looking directly at the camera with soft brown eyes. Lips are slightly parted, holding a thin black elastic hair tie between them"
  pose:
    action: "Sitting on a bed. Both arms are raised and bent behind her head, actively gathering her long dark brown hair to tie it into a high ponytail"
outfit:
  clothing: "A fitted brown ribbed knit spaghetti-strap camisole tank top that hugs her torso"
composition:
  type: "Candid high-angle bedroom selfie"
  layout: "Vertical smartphone selfie shot from a high angle, capturing the subject sitting on the bed with a large window and city skyline in the background"
environment:
  setting: "Modern high-rise apartment bedroom"
  background_details: "Floor-to-ceiling window revealing a bright city skyline of tall buildings. The subject is surrounded by white rumpled bedsheets, a cream fleece blanket, and a white pillow"
constraints:
  - "Must use the uploaded reference image as the absolute single source of truth for the subject's identity"
  - "Maintain 100% facial and identity consistency with the referenced subject"
  - "ALL text elements rendered in the image MUST be strictly in Vietnamese"
  - "Ensure the pose of tying hair with arms raised and holding the tie in the mouth is naturally and accurately depicted"
negative_prompt:
  - "over polished, plastic skin, studio flash, heavy makeup, oversexualized"
  - "deformed hands, extra fingers, missing fingers, bad anatomy"
  - "english text, cartoon, CGI, 3D render, flat colors"
