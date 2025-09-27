import streamlit as st
import instaloader
import os
import shutil

st.set_page_config(page_title="Instagram Video Downloader Only", layout="centered")
st.title("🎥 Instagram Video Downloader (Only Video)")

url = st.text_input("🔗 Enter Instagram Post URL")

def clean_instagram_url(insta_url: str) -> str:
    # Remove query params
    if "?" in insta_url:
        insta_url = insta_url.split("?")[0]

    # Replace /p/ with /reels/
    insta_url = insta_url.replace("/p/", "/reels/")
    insta_url = insta_url.rstrip("/")

    return insta_url

def download_video_only(insta_url):
    # Clean the URL first
    insta_url = clean_instagram_url(insta_url)

    # Clear old downloads
    if os.path.exists("downloads"):
        shutil.rmtree("downloads")
    os.makedirs("downloads", exist_ok=True)

    # Extract shortcode
    shortcode = insta_url.split("/")[-1]

    # Initialize Instaloader: disable other junk
    L = instaloader.Instaloader(
        dirname_pattern="downloads",
        save_metadata=False,
        download_comments=False,
        download_video_thumbnails=False,
        compress_json=False,
        post_metadata_txt_pattern=""   # disables that .txt metadata file
    )

    post = instaloader.Post.from_shortcode(L.context, shortcode)

    if post.is_video:
        # Download the video only
        L.download_post(post, target="")

        # Keep only .mp4 file, delete everything else
        video_path = None
        for file in os.listdir("downloads"):
            if file.endswith(".mp4"):
                video_path = os.path.join("downloads", file)
            else:
                os.remove(os.path.join("downloads", file))  # remove junk files

        return video_path
    else:
        return "NOT_VIDEO"


# ---- UI Logic ----
if url:
    clean_url = clean_instagram_url(url)
    st.info(f"✅ Cleaned URL: {clean_url}")

    if st.button("📥 Download Video"):
        result = download_video_only(url)

        if result == "NOT_VIDEO":
            st.warning("⚠️ This post is not a video. Please provide a video URL.")
        elif result:
            with open(result, "rb") as file:
                st.success("🎉 Video ready for download!")
                st.download_button("⬇️ Download Video", file, file_name=os.path.basename(result))
        else:
            st.error("❌ Unable to fetch the video. Make sure the link is public and valid.")