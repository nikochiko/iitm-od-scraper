# iitm-od-scraper
Automatically collect links to assignments and videos from IITM Online Degree

### How to use?
Clone the repo, create and activate a virtualenv if you want. Then run `pip install -r requirements.txt` from the clone directory.

If you're enrolled as a student at https://app.onlinedegree.iitm.ac.in, sign in to it with Google,
use Shift + F9 (Firefox, Chrome) to open the Storage tab in browser developer tools. From there, copy
the value in the `token` field of `id_token`key. Rename .env.example to .env, and replace your token
key in it.

Now, you can simply run `python scrape_videos.py $namespace_of_course`. Where namespace of course is the part like `ns_20t_...` 
at the end of the URL when you open courses in the Online Degree app.

## NOTE:
Using this scraper could be potentially against the IITM Online Degree's Copyright Policy. The user of this code is responsible
for his/her own actions and I (the author, nikochiko) shall not be held liable.
