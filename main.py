import datetime
import os
import json
import time
import urllib.request


def get_page(page):
    request = urllib.request.Request(page)
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0')
    return urllib.request.urlopen(request).read()


folder = './images/'

# Remove all pre-existing images
if os.path.isdir(folder):
    print("Cleaning images folder")
    os.system("rm -rf " + folder)
    os.system("git rm -r " + folder)

# Ensure the images folder exists
if not os.path.isdir(folder):
    os.mkdir(folder)

hasMore = True
page = 0
images = []

while hasMore:
    print("Loading page", page)
    response = get_page("https://undraw.co/api/illustrations?page=" + str(page))

    data = json.loads(response.decode('utf-8'))
    hasMore = data['hasMore']
    page = data['nextPage']

    for illustration in data['illos']:
        images.append((
            illustration['title'].replace(" ", "_").lower(),
            illustration['image']
        ))

print("Loaded all pages")

titles = [image[0] for image in images]
file = open("titles.js", 'w')
file.write('export default ')
file.write(json.dumps(titles, indent=2))
file.close()

for i in range(len(images)):
    name, location = images[i]
    image = get_page(location)

    fname = folder + name + '.svg'
    file = open(fname, 'w')
    file.write(image.decode('utf-8'))
    file.close()

    print("[%04d/%04d] Downloaded %s" % (i + 1, len(images), name))

    os.system("git add \"%s\"" % fname)
    time.sleep(0.5)

date = datetime.datetime.now().strftime("%Y-%m-%d")
os.system("git commit -m \"Images %s\"" % date)
