# The 3-Minute Decision — Mars Rover Challenge

A mobile-friendly, interactive **Streamlit** educational game about making evidence-based choices when a fictional Mars rover cannot receive an immediate response from Earth.

## What's included

- Six different rover emergencies, each with a **180-second live countdown**.
- Three decision choices per scenario, including consequences and engineering lessons.
- Easy-to-read telemetry cards, engineering notes, and optional decision explanations.
- Mission resources: **Safety, Energy, Science** (0–100 each), with points and a final performance report.
- Downloadable CSV decision log, restart option, original Mars artwork, and an app icon.
- Responsive dark theme, phone-friendly navigation, large aligned buttons.
- No usernames, teacher names, school names, tracking services, or user accounts.

> **Educational simulation:** All emergency scenarios, telemetry numbers, resource deltas, and scores are fictional and simplified. NASA does not sponsor or endorse this game. NASA describes communication delays of roughly 4–24 minutes **one way** between Earth and Mars, depending on planetary distance. Our **3 minutes** are the game's decision window, not a signal-travel time.

## Files you need to keep together

```text
mars-3-minute-decision/
├── app.py                     ← Main Streamlit app
├── requirements.txt           ← Python dependencies
├── assets/
│   ├── mars_hero.png           ← Original header illustration
│   └── app_icon.png            ← Original app/favicon image
└── .streamlit/
    └── config.toml            ← Consistent, accessible dark theme
```

## Deploy with GitHub and Streamlit (no coding required)

1. Download the project ZIP, then **extract** the ZIP on your computer. **Do not upload the ZIP itself** as the app file.
2. Visit [GitHub](https://github.com), sign in, select **New repository** and call it `mars-3-minute-decision`. Select **Public**, then create the repository.
3. Click **Add file → Upload files**. Drag the *contents* of the extracted project folder into GitHub so `app.py` and `requirements.txt` appear at the repository's top level, and `assets/` and `.streamlit/` preserve their folders. (Alternatively, upload all four/five files using their folder paths.)
4. Click **Commit changes**.
5. Open [Streamlit Community Cloud](https://share.streamlit.io). Click **Create app** / **New app**, choose the repository and `main` branch, and set the main file path to **`app.py`**.
6. Click **Deploy**. Then open the new `*.streamlit.app` link on your phone.

### Put an app icon on the phone's home screen

On Android Chrome: open your app URL → tap **⋮** → **Add to Home screen** → **Create shortcut** / **Install**, if offered. This creates a shortcut to the web app; it is **not a native Android APK**. The included icon sets the web page's favicon, but the exact shortcut icon depends on the browser.

## Run locally (optional)

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Privacy

The application does not request accounts or personal details. Responses and notes are stored only in the current Streamlit session in memory. They are not stored in a database. Users can download their own responses as a CSV report. Streamlit hosting services may still collect normal service access logs under their own policies.

## Learning sources

- NASA: [Space Communications: 7 Things You Need to Know](https://www.nasa.gov/centers-and-facilities/goddard/space-communications-7-things-you-need-to-know/)
- NASA: [How Perseverance Drives on Mars](https://science.nasa.gov/resource/how-perseverance-drives-on-mars/)
- NASA: [Perseverance Rover Components](https://science.nasa.gov/mission/mars-2020-perseverance/rover-components/)

**All illustrated artwork in the app was created for this project; no externally hosted images are required.**
