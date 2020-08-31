import requests
from io import BytesIO
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif(url):
	response = requests.get(url)
	image = Image.open(BytesIO(response.content))
	image.verify()
	return image._getexif()

def get_labeled_exif(exif):
	if not exif:
		raise ValueError('No EXIF metadata found')

	labeled = {}
	for (key, val) in exif.items():
		labeled[TAGS.get(key)] = val
	return labeled

def get_geotagging(exif):
	if not exif:
		raise ValueError('No EXIF metadata found')

	geotagging = {}
	for (idx, tag) in TAGS.items():
		if tag == 'GPSInfo':
			if idx not in exif:
				raise ValueError('No Geotagging data found')

			for (key, value) in GPSTAGS.items():
				if key in exif[idx]:
					geotagging[value] = exif[idx][key]

	return geotagging

def get_decimal_from_dms(dms, ref):
	degrees = dms[0]
	minutes = dms[1] / 60.0
	seconds = dms[2] / 3600.0

	if ref in ['S', 'W']:
		degrees = -degrees
		minutes = -minutes
		seconds = -seconds

	return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
	lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
	lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

	return (lat,lon)

exif = get_exif('https://images.unsplash.com/photo-1523115450297-f3ad48ed1574')
labeled = get_labeled_exif(exif)
geotags = get_geotagging(exif)
# print(geotags)
coords = get_coordinates(geotags)
print(coords)
