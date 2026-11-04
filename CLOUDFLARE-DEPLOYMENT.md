# Cloudflare Pages deployment

Connect this GitHub repository to a Cloudflare Pages project.

- Production branch: main
- Framework preset: None
- Root directory: repository root (leave blank)
- Build command: sh build.sh
- Build output directory: dist

The build extracts only public website assets from BHS-Fitchburg-Professional-Website.zip. The Python server, environment example and internal README are not published.

The Pages Function at /api/contact returns an explicit unavailable response. No form data is saved or forwarded by this handler. Enable contact delivery only after approving the backend, security, privacy workflow and applicable vendor agreements.

The included Python server does not run on this Pages deployment.

After deploying, verify the actual Cloudflare-provided URL, images, service pages, mobile layout, phone links and form error message. No live URL is claimed until deployment is confirmed.
