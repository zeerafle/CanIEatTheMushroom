import reflex as rx
from dotenv import load_dotenv

_ = load_dotenv()

config = rx.Config(
    app_name="app",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
