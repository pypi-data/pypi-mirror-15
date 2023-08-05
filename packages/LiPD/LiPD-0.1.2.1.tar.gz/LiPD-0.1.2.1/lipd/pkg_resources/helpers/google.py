import urllib.request
import urllib.parse
import urllib.error

import io
from .MapFrame import *

# GLOBALS
APPLICATION_NAME = 'lipd'
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'


def get_google_csv(file_id, filename):
    """
    Get a specific spreadsheet file from Google Drive using its FILE_ID.
    Write the spreadsheet on the local system as a CSV.
    TSNames ID: 1C135kP-SRRGO331v9d8fqJfa3ydmkG2QQ5tiXEHj5us
    :param file_id: (str) Google File ID of target file
    :param filename: (str) Optional: Override filename from google your specified filename
    :return: (str) CSV Filename
    """
    # Download link format
    link_csv = 'https://docs.google.com/spreadsheet/ccc?key=' + file_id + '&output=csv&pref=2'

    try:
        urllib.request.urlretrieve(link_csv, filename)
    except Exception:
        print("Error retrieving {}".format(filename))
    return filename


def get_static_google_map(filename_wo_ext, center=None, zoom=None, imgsize=(640,640), imgformat="jpeg",
                          maptype="hybrid", markers=None):
    """
    Retrieve a map (image) from the static google maps server

    Source: http://code.google.com/apis/maps/documentation/staticmaps/
    Source: http://hci574.blogspot.com/2010/04/using-google-maps-static-images.html

    Creates a request string with a URL, looks like:
    http://maps.google.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=14&size=512x512&maptype=roadmap
    &markers=color:blue|label:S|40.702147,-74.015794&sensor=false

    :param filename_wo_ext: (str) Filename without extension
    :param center: (tuple of ints) Location to center the map frame
    :param zoom: (int) Zoom amount from 0 (world) to 22 (streets)
    :param imgsize: (tuple of ints) Map image size (max. 640x640)
    :param imgformat: (str) Image format (jpg, bmp, png)
    :param maptype: (str) Map Type (roadmap, satellite, hybrid, terrain)
    :param markers: (list of str) Strings holding marker attributes

    """

    # Assemble the base URL. Append parameters separated by &
    request = "http://maps.google.com/maps/api/staticmap?"

    # If center and zoom  are not given, the map will show all marker locations
    if center is not None:
        request += "center=%s&" % center
    if center is not None:
        request += "zoom=%i&" % zoom

    request += "size=%ix%i&" % imgsize
    request += "format=%s&" % imgformat
    request += "maptype=%s&" % maptype

    # Add markers (location and style)
    if markers is not None:
        for marker in markers:
                request += "%s&" % marker

    # optional: mobile=true assumes the image is shown on a small screen
    # request += "mobile=false&"

    # required, deals with getting location from mobile device
    request += "sensor=false&"
    # print(request)

    # Option 1: save image directly to disk
    # urllib.request.urlretrieve(request, "testing_map."+imgformat)

    # Option 2: read into PIL
    web_sock = urllib.request.urlopen(request)
    img_data = io.BytesIO(web_sock.read())  # constructs a StringIO holding the image

    try:
        # save image to disk, but then open it in Tkinter dialog box
        # if center is None:
        #     center = ''
        pil_img = Image.open(img_data)
        # Display image saved on disk
        # Show image in default image viewer
        pil_img.show()
        # Save as jpg
        pil_img.save(filename_wo_ext+".jpg", "JPEG")
        # m = Tk()
        # m.frame = MapFrame(m, pil_img, str(center))
        # m.mainloop()

    # if this cannot be read as image, it's probably an error from the server,
    except IOError:
        print("IOError:" + str(img_data.read()))  # print error (or it may return a image showing the error"

