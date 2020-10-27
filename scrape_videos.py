import json
import os
import sys

import requests
from dotenv import load_dotenv


load_dotenv()


SEEK_TOKEN = os.getenv("SEEK_ID_TOKEN")
BACKEND_URL = "https://backend.seek.onlinedegree.iitm.ac.in/graphql"
USER_AGENT = "Altruist Scraper (by gh/nikochiko)"


QUERY_COURSE = """\
query course($namespace: String!) {
  course(namespace: $namespace) {
    courseOutlineWithChildrenOrder
    title
    blurb
    mainImageDumped
    forumUrl
    __typename
  }
}
"""

QUERY_LESSON = """\
query lesson($id_: String!, $namespace: String!) {
  lesson(id_: $id_, namespace: $namespace) {
    title
    video
    parentUnitId
    transcriptVttUrl
    objectives
    lessonId
    __typename
  }
}
"""


def get_course(ns):
    r = requests.post(
        BACKEND_URL,
        data={"query": QUERY_COURSE, "variables": json.dumps({"namespace": ns})},
        headers={
            "SEEK_ID_TOKEN": SEEK_TOKEN,
            "User-Agent": USER_AGENT,
            "SEEK_NAMESPACE": ns,
        },
    )
    resp = r.json()
    if not resp.get("errors"):
        return resp["data"]["course"]
    else:
        raise Exception(
            f"Error while trying to fetch data from backend:\n{resp['errors']}"
        )


def get_lesson_video_url(ns, lesson_id):
    r = requests.post(
        BACKEND_URL,
        data={
            "query": QUERY_LESSON,
            "variables": json.dumps({"namespace": ns, "id_": lesson_id}),
        },
        headers={
            "SEEK_ID_TOKEN": SEEK_TOKEN,
            "User-Agent": USER_AGENT,
            "SEEK_NAMESPACE": ns,
        },
    )
    resp = r.json()
    if not resp.get("errors"):
        return f"https://youtube.com/watch?v={resp['data']['lesson']['video']}"
    else:
        raise Exception(
            f"Error while trying tof etch data from backend:\n{resp['errors']}"
        )


def scrape_ns_for_videos(ns):
    course = get_course(ns)
    course_children = json.loads(course["courseOutlineWithChildrenOrder"])
    sections = {}
    for section in course_children:
        sec_name = section["title"]
        sections[sec_name] = {}
        for child in section.get("children", []):
            if child["type"] == "lesson" and child["has_video"] == True:
                sections[sec_name][child["title"]] = get_lesson_video_url(
                    ns, child["id"]
                )
    return sections


def make_neat_markdown(sections):
    retval = ""
    for (sec, lessons) in sections.items():
        retval += f"## {sec}\n\n"
        for (lesson, video) in lessons.items():
            retval += f"* [{lesson}]({video})\n"
    return retval


def make_neat_html(sections):
    retval = "<html><head><title>IITM-OD Scrapr by gh/nikochiko</title></head><body>"
    for (sec, lessons) in sections.items():
        retval += f"<h2>{sec}</h2>\n<ul>"
        for (lesson, video) in lessons.items():
            retval += f"<li><a href=\"{video}\" target=\"_blank\">{lesson}</a></li>\n"
        retval += "</ul></body></html>"
    return retval


if __name__ == "__main__":
    if len(sys.argv) == 2:
        ns = sys.argv[1]
        html = make_neat_html(scrape_ns_for_videos(ns))
        fpath = f"./iitmod_videos_{ns}.html"
        with open(fpath, "w") as f:
            print(html)
            f.write(html)
        print(f"Written to file {fpath}")
    else:
        print("Try something like: 'python scrape_videos.py ns_20t1_cs1001'")
