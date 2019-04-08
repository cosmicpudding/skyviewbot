# SkyviewBot
SkyviewBot: base repo to go alongside "Good Coding Practice" (ASTERICS-OBELICS 2019).   
See also GCP talk slides: https://drive.google.com/open?id=1vdV290w_2hsvVmsoXKdgTo1hQuGxMhlU

### Overview
The main goal of this repository is to introduce three primary concepts in good coding practices: 1) argument parsing, 2) modularisation, and 3) docstrings. The code will "run" as it is (once the setup is done), but there are many ways to improve on what it does with better structure and more customised options.

The overall flow:
1) Download a FITS cutout from any of the 100+ Skyview surveys (or use pre-existing FITS)
2) Use APLpy to make an image of the FITS file with custom settings
3) Upload the resulting image to Google Drive using PyDrive wrapper around REST API
4) Attach the web-ready image to a Slack post and send to the #gcp channel

The best image post will win a box of world-famous Dutch stroopwafels. 

### Dependencies:
- APLpy: http://aplpy.readthedocs.io
- PyDrive: https://pythonhosted.org/PyDrive

### Things you need to do to get this running:
1) `git pull origin master` in School 2019, `conda env update -f environment.yml` (from T. Dijkema)
2) **Preferred: fork this repository, then `git clone` your version so you can push changes back**  
Alternative: `git clone https://github.com/cosmicpudding/skyviewbot.git` to a sensible location
3) Download `skyview.jar`: https://skyview.gsfc.nasa.gov/current/jar/skyview.jar
4) Move `skyview.jar` to the main code folder (or change the path in `call_skyview()`
5) When first running code: authenticate using autoskyview@gmail.com login details for Google Drive API
6) Join the #gcp channel on http://obelics-school.slack.com (GCP = Good Coding Practices)

### If you get stuck
- ask your neighbour
- ask a tutor
- `@vamoss` on http://obelics-school.slack.com (`#gcp` channel or DM)

