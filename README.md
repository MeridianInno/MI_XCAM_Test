# MI_XCAM_rgb2temp_example
This is the sample code of showing how to convert RGB value captured by videoCapture object to temperature value on Python.


Settings
- XCAM_single (YUYV output thermal image)
- Non-adaptive color mapping mode
- Using defalut colorPalette0
- SetTempDisplay(0)

createColorTable() : create the color table following the same algorithm on MCU, it is firmware dependent
find_nearest(array, value): find the nearest point that matching to the target RGB value, since the cap.read() convert the YUYV stream to                               BGR internally, the convertion makes precision issue, which is why we cannot directly mapping by comparing RGB only. Also openCV does not support getting YUYV raw streaming but BGR.

"frame" is the raw data captured by cap.read() which is in BGR color space in size of 192x192, 6 times enlarged from 32x32.
Please refers to XCAM thermal sensor SDK for more firmware details.
https://github.com/MeridianInnovation/MI_XCAM_formalRelease
