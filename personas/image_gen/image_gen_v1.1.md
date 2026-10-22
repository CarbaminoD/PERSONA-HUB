prompt:
  type: "Nighttime City Selfie Photography"
  aspect_ratio: "3:4 vertical"
  style: "Candid mobile phone selfie, authentic night city portrait"
  quality: "Mobile phone camera quality, natural texture, soft ambient glow"
global_instructions:
  character_consistency: "Hình ảnh tạo ra phải là 1 người duy nhất, và luôn lấy dữ liệu tham chiếu từ hình ảnh upload kèm đoạn prompt này để đảm bảo sự nhất quán tuyệt đối về khuôn mặt."
  text_requirements: "Nếu có văn bản xuất hiện trên ảnh thì bắt buộc phải là tiếng Việt."
character:
  demographics:
    age: "in her twenties"
    gender: "woman"
    ethnicity: "Japanese, East Asian"
  facial_extraction:
    instructions: "Trích xuất từ ảnh upload: Hình dáng khuôn mặt, đặc điểm ngũ quan, màu mắt, kiểu tóc v.v. Extracted strictly from the uploaded input source image. Do not change the underlying face structure. Preserve exact facial features, identity, proportions, skin texture, age, and facial structure. Do not redesign, beautify, or stylize. The generated subject must be the exact same person as the reference in this single image."
    features:
      face_shape: "Exact match to reference image"
      eyes: "Exact match to reference image, including exact eye color"
      nose: "Exact match to reference image"
      lips: "Exact match to reference image"
      skin: "Exact match to reference image"
      hair: "Exact match to reference image's base hair color and style"
  physical_details:
    hair: "Mái tóc đen dài với tóc mái (giữ nguyên màu và kiểu tóc cơ bản từ ảnh tham chiếu)"
    expression: "Biểu cảm trung tính mềm mại"
    gaze: "looking at camera"
  pose:
    type: "Selfie pose"
    camera_gaze: "looking at camera"
outfit:
  clothing: "Váy yếm ren màu đỏ đậm với lỗ khóa hở, khoe khe ngực và có viền ren tinh tế dọc theo mép cổ áo"
  details: "Delicate lace trim along the edges of the neckline"
  accessories:
    - "Vòng cổ vàng mỏng quanh cổ"
composition:
  type: "Single image"
  framing: "Một hình ảnh đơn, chụp tự sướng góc cao của một phụ nữ duy nhất"
  angle: "High angle shot"
environment:
  setting: "City background"
  time_of_day: "Nighttime"
  background_details: "Blurred building lights and windows"
lighting:
  ambient: "Dim ambient lighting"
  effects: "Soft glow on her face"
camera_settings:
  angle: "High angle shot"
  quality: "Mobile phone camera quality"
negative_prompt:
  - "plastic skin, over-smoothed, deformed hands, extra fingers, missing fingers"
  - "bad anatomy, inconsistent face, changing clothes, cluttered background"
  - "text, watermark, logo"
