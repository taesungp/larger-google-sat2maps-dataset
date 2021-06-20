from PIL import Image
from urllib.request import urlopen
import numpy as np
import os
import pymp
import glob
import hashlib
import hmac
import base64
import urllib.parse as urlparse

API_key = "GOOGLE API KEY NEEDED"
SECRET = "GOOGLE SECRET API KEY NEEDED"

def sign_url(input_url=None, secret=None):
    """ Sign a request URL with a URL signing secret.
      Usage:
      from urlsigner import sign_url
      signed_url = sign_url(input_url=my_url, secret=SECRET)
      Args:
      input_url - The URL to sign
      secret    - Your URL signing secret
      Returns:
      The signed request URL
  """

    if not input_url or not secret:
        raise Exception("Both input_url and secret are required")

    url = urlparse.urlparse(input_url)

    # We only need to sign the path+query part of the string
    url_to_sign = url.path + "?" + url.query

    # Decode the private key into its binary format
    # We need to decode the URL-encoded private key
    decoded_key = base64.urlsafe_b64decode(secret)

    # Create a signature using the private key and the URL-encoded
    # string using HMAC SHA1. This signature will be binary.
    signature = hmac.new(decoded_key, str.encode(url_to_sign), hashlib.sha1)

    # Encode the binary signature into base64 for use within a URL
    encoded_signature = base64.urlsafe_b64encode(signature.digest())

    original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query

    # Return signed URL
    return original_url + "&signature=" + encoded_signature.decode()

coords = [(40.99140532100601, -74.36558281324726), (40.583818214918885, -73.60340628434221), "New York",
          (34.27184742446742, -118.61248422231873), (33.76761980811145, -117.78748679566478), "Los Angeles",
          (34.186810868492714, -118.0106956484995), (33.840354873779646, -117.15506171263294), "Los Angeles",
          (42.227976171796975, -88.43817444533049), (41.54467865612732, -87.4827320651874), "Chicago",
          (30.03349866405033, -95.71580775901401), (29.459992704019207, -94.92067224507522), "Houston",
          (33.85522166434143, -112.40523353799817), (33.298023178042094, -111.73369421793589), "Pheonix",
          (40.138507167269466, -75.37346754328397), (39.88765325903279, -74.9937525698745), "Philly",
          (29.631654748402877, -98.73279051108209), (29.2333723023254, -98.24115231766226), "San Antonio",
          (32.93034750083633, -117.2683116967088), (32.634778464777014, -116.94284171950069), "San Diego",
          (33.055705530078335, -97.1854330926876), (32.663493787186646, -96.6107107911619), "Dallas",
          (37.42394341818442, -122.10993134584604), (37.22300174123166, -121.75630890225493), "San Jose",
          (30.45814177688897, -97.9305640280481), (30.21575922329494, -97.60921392396921), "Austin",
          (30.51424486821616, -81.86988256205164), (30.186570086869477, -81.44278904765619), "Jacksonville",
          (33.216237563645386, -97.49122422868892), (32.54965767190676, -96.97898666962301), "Fort Worth",
          (40.132650427161614, -83.17417046570878), (39.851734474710995, -82.78621574604091), "Columbus",
          (35.311286613977266, -80.97579238309578), (35.06886697575736, -80.69358107374445), "Charlotte",
          (37.80382411867336, -122.51141485348941), (37.71140093593331, -122.38232549544063), "San Francisco",
          (39.922556770385775, -86.31265826077322), (39.64183435316462, -85.95216936196678), "Indianapolis",
          (47.732233006039955, -122.41897499511806), (47.50822491126062, -122.25212013338479), "Seattle",
          (39.93084143486826, -105.20736773839866), (39.56604069864837, -104.78027422400321), "Denver",
          (38.99797884601219, -77.22400469444615), (38.79463801506532, -76.89441484410882), "Washington DC",
          (42.45304469755918, -71.2713797753314), (42.25667277053182, -70.98504859285084), "Boston",
          ]

cities = []

areas = []
for i in range(0, len(coords), 3):
    name = coords[i + 2]
    topleft = coords[i]
    bottomright = coords[i + 1]
    h = bottomright[0] - topleft[0]
    w = bottomright[1] - topleft[1]
    area = h * w

    cities.append((topleft[0], topleft[1], h, w, name))
    areas.append(area)
    
probs = np.array(areas) / np.sum(areas)

outdir = "./out/"
os.makedirs(outdir, exist_ok=True)

# find existing indices
existing_files = glob.glob(os.path.join(outdir, "*.png"))
existing_indices = [int(os.path.basename(filename).split("_")[0]) for filename in existing_files]

num_images = 300
city_indices = np.random.choice(len(areas), size=(num_images), p=probs)
random_coords = np.random.rand(num_images, 2)
with pymp.Parallel(16) as p:
    for i in p.range(0, num_images):
        if i in existing_indices:
            continue
        city_idx = city_indices[i]

        y, x, h, w, name = cities[city_idx]
        loc = (y + h * random_coords[i, 0], x + w * random_coords[i, 1])

        savename = "%06d_%s_%.5f_%.5f.png" % (i, name.replace(" ", "_"), loc[0], loc[1])
        
        styles = ["satellite", "roadmap"]
        
        out = Image.new('RGB', (1024, 512))
        for j, style in enumerate(styles):
            url = "https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom=17&size=640x640&maptype={}&style=feature:all%7Celement:labels%7Cvisibility:off&key={}".format(loc[0], loc[1], style, API_key)
            url = sign_url(url, SECRET)
            im = Image.open(urlopen(url))
            im = im.crop((0, 0, 512, 512))
            out.paste(im, (512 * j, 0))
        out.save(os.path.join(outdir, savename))
        if i % 10 == 0:
            print(savename)
        
    

