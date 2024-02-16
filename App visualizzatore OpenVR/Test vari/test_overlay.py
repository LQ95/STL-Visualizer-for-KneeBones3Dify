import openvr

def main():
	openvr.VR_Init(openvr.VRApplication_Overlay)
	

	handle= openvr.VROverlayHandle_t
	openvr.VROverlay().CreateOverlay ("image", "image", handle) # key has to be unique, name doesn't matter 
	openvr.VROverlay().SetOverlayFromFile(handle, "example.jpg")
	openvr.VROverlay().SetOverlayWidthInMeters(handle, 3)
	openvr.VROverlay().ShowOverlay(handle)
	transform = [
		[1.0, 0.0, 0.0, 0.0],
		[0.0, 1.0, 0.0, 1.0],
		[0.0, 0.0, 1.0, -2.0]
	]
	openvr.VROverlay().SetOverlayTransformAbsolute(handle, TrackingUniverseStanding, transform)
	while (true):
		i=1