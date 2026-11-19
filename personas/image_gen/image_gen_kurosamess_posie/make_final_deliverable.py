import cv2
import numpy as np
from scipy.interpolate import RBFInterpolator, CubicHermiteSpline

# 1. Load target and ref1
target = cv2.imread(r'personas\image_gen\image_gen_kurosamess_posie\kurosamess_01.jpg')
ref1 = cv2.imread(r'personas\image_gen\image_gen_kurosamess_posie\th-11134207-81ztc-mrdz7j1nwagw31.jpg')

# 2. Inpaint hair AND strings on ref1 (pure clean skin, buttons, and lace)
h, w = ref1.shape[:2]
gray = cv2.cvtColor(ref1, cv2.COLOR_BGR2GRAY)

hair_mask = np.zeros((h, w), dtype=np.uint8)
roi = (gray[520:700, 550:620] < 80).astype(np.uint8) * 255
roi = cv2.dilate(roi, np.ones((7, 7), np.uint8))
hair_mask[520:700, 550:620] = roi

string_mask = np.zeros((h, w), dtype=np.uint8)
cv2.line(string_mask, (515, 465), (512, 568), 255, thickness=8)
cv2.line(string_mask, (515, 465), (524, 568), 255, thickness=8)

clean_mask = cv2.bitwise_or(hair_mask, string_mask)
ref1_clean = cv2.inpaint(ref1, clean_mask, 5, cv2.INPAINT_TELEA)

# 3. Dual-zone Reinhard color transfer
ref1_lab = cv2.cvtColor(ref1_clean, cv2.COLOR_BGR2LAB).astype(np.float32)

src_fab = ref1_clean[530:580, 420:450]
tgt_fab = target[850:950, 480:530]
src_fab_lab = cv2.cvtColor(src_fab, cv2.COLOR_BGR2LAB).astype(np.float32)
tgt_fab_lab = cv2.cvtColor(tgt_fab, cv2.COLOR_BGR2LAB).astype(np.float32)

ref1_fab_matched = ref1_lab.copy()
for ch in range(3):
    sm, ss = src_fab_lab[:, :, ch].mean(), src_fab_lab[:, :, ch].std()
    tm, ts = tgt_fab_lab[:, :, ch].mean(), tgt_fab_lab[:, :, ch].std()
    ref1_fab_matched[:, :, ch] = (ref1_lab[:, :, ch] - sm) * (ts / (ss + 1e-5)) + tm

src_skin = ref1_clean[490:540, 495:530]
tgt_skin = target[800:830, 600:650] # Pure skin sample away from strings
src_skin_lab = cv2.cvtColor(src_skin, cv2.COLOR_BGR2LAB).astype(np.float32)
tgt_skin_lab = cv2.cvtColor(tgt_skin, cv2.COLOR_BGR2LAB).astype(np.float32)

ref1_skin_matched = ref1_lab.copy()
for ch in range(3):
    sm, ss = src_skin_lab[:, :, ch].mean(), src_skin_lab[:, :, ch].std()
    tm, ts = tgt_skin_lab[:, :, ch].mean(), tgt_skin_lab[:, :, ch].std()
    ref1_skin_matched[:, :, ch] = (ref1_lab[:, :, ch] - sm) * (ts / (ss + 1e-5)) + tm

Y, X = np.ogrid[:h, :w]
keyhole_ellipse = ((X - 515.0)/36.0)**2 + ((Y - 525.0)/52.0)**2 < 1.0
bgr = ref1_clean.astype(np.float32)
skin_cond = (bgr[:, :, 2] - bgr[:, :, 0] > 20) & keyhole_ellipse
skin_mask = cv2.GaussianBlur(skin_cond.astype(np.float32), (9, 9), 3.0)[:, :, None]

combined_lab = ref1_skin_matched * skin_mask + ref1_fab_matched * (1.0 - skin_mask)
ref1_dual = cv2.cvtColor(np.clip(combined_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)

# 4. Verified 13 control points
src_pts = np.array([
    [515, 465], # knot
    [480, 485], # l_top
    [545, 485], # r_top
    [461, 525], # l_mid
    [556, 525], # r_mid
    [485, 555], # l_low
    [535, 555], # r_low
    [513, 577], # b1
    [518, 604], # b2
    [519, 630], # b3
    [430, 575], # l_outer
    [570, 575], # r_outer
    [518, 655], # hem
], dtype=np.float32)

dst_pts = np.array([
    [635, 660],
    [590, 680],
    [650, 680],
    [590, 830], # l_mid
    [740, 845], # r_mid
    [595, 935], # l_low
    [685, 935], # r_low
    [628, 977], # b1
    [627, 1008], # b2
    [626, 1039], # b3
    [520, 935], # l_outer
    [760, 935], # r_outer
    [626, 1060], # hem
], dtype=np.float32)

ymin, ymax = 770, 1070
xmin, xmax = 510, 785
grid_y, grid_x = np.mgrid[ymin:ymax, xmin:xmax]
grid_dst = np.column_stack([grid_x.ravel(), grid_y.ravel()])

rbf = RBFInterpolator(dst_pts, src_pts, kernel='thin_plate_spline')
grid_src = rbf(grid_dst)

src_x = grid_src[:, 0].reshape(ymax - ymin, xmax - xmin).astype(np.float32)
src_y = grid_src[:, 1].reshape(ymax - ymin, xmax - xmin).astype(np.float32)

warped_nostr = cv2.remap(ref1_dual, src_x, src_y, cv2.INTER_CUBIC)

# 5. Polygon definition covering Shrek:
poly = np.array([
    [548, 826],
    [768, 846],
    [754, 1054],
    [530, 1036],
], dtype=np.int32)

# Illumination matching
boundary_pts = []
boundary_diffs = []
edges = [
    (poly[0], poly[1]), # Top
    (poly[1], poly[2]), # Right
    (poly[2], poly[3]), # Bottom
    (poly[3], poly[0]), # Left
]

for p1, p2 in edges:
    for alpha in np.linspace(0, 1, 40):
        pt = (1 - alpha) * p1 + alpha * p2
        x, y = int(round(pt[0])), int(round(pt[1]))
        t_val = target[y, x].astype(np.float32)
        w_val = warped_nostr[y - ymin, x - xmin].astype(np.float32)
        
        # In string crossing region on top edge, clamp to pure skin
        if y < 850 and 675 <= x <= 725 and np.mean(t_val) > 220:
            t_val = np.array([182.0, 215.0, 248.0], dtype=np.float32)
            
        boundary_pts.append([x - xmin, y - ymin])
        boundary_diffs.append(t_val - w_val)

boundary_pts = np.array(boundary_pts, dtype=np.float32)
boundary_diffs = np.array(boundary_diffs, dtype=np.float32)

grid_pts = np.column_stack([grid_x.ravel(), grid_y.ravel()])
rbf_illum = RBFInterpolator(boundary_pts, boundary_diffs, kernel='linear', smoothing=10.0)
illum_field = rbf_illum(grid_pts).reshape(ymax - ymin, xmax - xmin, 3)

warped_illum = np.clip(warped_nostr.astype(np.float32) + illum_field, 0, 255).astype(np.uint8)

# 6. SeamlessClone without strings
poly_patch = poly - np.array([xmin, ymin])
mask = np.zeros((ymax - ymin, xmax - xmin), dtype=np.uint8)
cv2.fillPoly(mask, [poly_patch], 255)

rx, ry, rw, rh = cv2.boundingRect(mask)
center = (xmin + rx + rw // 2, ymin + ry + rh // 2)

res = cv2.seamlessClone(warped_illum, target, mask, center, cv2.NORMAL_CLONE)

# 7. Restore target above y_cut across the entire chest
res_restored = res.copy()
for x in range(540, 765):
    y_cut = int(round(826.0 + 20.0 * (x - 548.0) / 220.0))
    for y in range(820, y_cut):
        res_restored[y, x] = target[y, x]

# 8. Smooth the skin seam with 31-pixel vertical cosine ramp across the keyhole opening
for x in range(590, 736):
    y_s = int(round(826.0 + 20.0 * (x - 548.0) / 220.0))
    y1 = y_s - 15
    y2 = y_s + 16
    col = res_restored[y1:y2, x].astype(float)
    col_smooth = cv2.blur(col, (1, 15))
    w_ramp = np.exp(-0.5 * ((np.arange(31) - 15.0) / 6.0)**2)[:, None]
    blended = col_smooth * w_ramp + col * (1.0 - w_ramp)
    res_restored[y1:y2, x] = np.clip(blended, 0, 255).astype(np.uint8)

# 9. Draw the 3 natural strings with exact C1 continuity starting from y=832.0:
# String 1: starts at (681.0, 832.0), incoming slope +0.45
y_knots1 = np.array([832.0, 870.0, 930.0, 990.0, 1025.0])
x_knots1 = np.array([680.5, 688.0, 693.0, 691.0, 688.0])
d_knots1 = np.array([+0.45, +0.15, 0.00, -0.05, -0.10])
spline1 = CubicHermiteSpline(y_knots1, x_knots1, d_knots1)

# String 2: starts at (706.0, 832.0), incoming slope +0.40
y_knots2 = np.array([832.0, 875.0, 925.0, 970.0])
x_knots2 = np.array([705.5, 713.0, 715.0, 711.0])
d_knots2 = np.array([+0.40, +0.15, 0.00, -0.10])
spline2 = CubicHermiteSpline(y_knots2, x_knots2, d_knots2)

# String 3: starts at (717.0, 832.0), incoming slope +0.20
y_knots3 = np.array([832.0, 870.0, 910.0, 935.0])
x_knots3 = np.array([716.8, 722.0, 722.0, 719.0])
d_knots3 = np.array([+0.20, +0.10, 0.00, -0.10])
spline3 = CubicHermiteSpline(y_knots3, x_knots3, d_knots3)

final_image = res_restored.copy()

def render_photorealistic_string(img, spline, y_start, y_end, width=3.4):
    ys = np.linspace(y_start, y_end, int((y_end - y_start) * 4))
    xs = spline(ys)
    pts = np.column_stack([xs, ys]).astype(np.float32)
    
    # 1. Left shadow: offset x=-2.0, y=+1.0
    shadow_mask = np.zeros(img.shape[:2], dtype=np.float32)
    cv2.polylines(shadow_mask, [np.int32([pts + np.array([-2.0, 1.0])])], isClosed=False, color=1.0, thickness=int(width + 2), lineType=cv2.LINE_AA)
    shadow_mask = cv2.GaussianBlur(shadow_mask, (5, 5), 1.2)
    
    # Shadow fade in over first 8 pixels and fade out at tip
    y_fade_in = np.clip((ys - y_start) / 8.0, 0.0, 1.0)
    y_fade_out = np.clip((y_end - ys) / 20.0, 0.0, 1.0)
    shadow_mult = shadow_mask * (0.16 * y_fade_in * y_fade_out)[:, None]
    
    for ch in range(3):
        img[:, :, ch] = np.clip(img[:, :, ch] * (1.0 - shadow_mult), 0, 255)
        
    # 2. String core
    core_mask = np.zeros(img.shape[:2], dtype=np.float32)
    cv2.polylines(core_mask, [np.int32([pts])], isClosed=False, color=1.0, thickness=int(width), lineType=cv2.LINE_AA)
    core_mask = cv2.GaussianBlur(core_mask, (3, 3), 0.7)
    
    # Fade core at tip
    core_mult = core_mask * y_fade_out[:, None]
    string_color = (222, 242, 252)
    for ch in range(3):
        img[:, :, ch] = np.clip(img[:, :, ch] * (1.0 - core_mult) + string_color[ch] * core_mult, 0, 255)

render_photorealistic_string(final_image, spline1, 832.0, 1025.0, width=3.4)
render_photorealistic_string(final_image, spline2, 832.5, 970.0, width=3.4)
render_photorealistic_string(final_image, spline3, 833.0, 935.0, width=3.1)

# Save final result directly to deliverable path!
output_path = r'D:\side-project\PersonaHub\personas\image_gen\image_gen_kurosamess_posie\kurosamess_01_mod.jpg'
cv2.imwrite(output_path, final_image, [cv2.IMWRITE_JPEG_QUALITY, 98])

# Also save inspection crops
cv2.imwrite(r'personas\image_gen\image_gen_kurosamess_posie\final_inspect_torso.jpg', final_image[400:1150, 400:900])
cv2.imwrite(r'personas\image_gen\image_gen_kurosamess_posie\final_inspect_zoom.png', final_image[800:880, 560:760])
print('Saved final deliverable at:', output_path)

