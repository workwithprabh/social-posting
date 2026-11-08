# Connecting Google Business Profile reviews (one-time setup)

`scripts/gbp_reviews.py` reads reviews through the Business Profile APIs with OAuth. Do this once, signed in as the
Google account that manages the dealers' Business Profiles. Nothing here goes into chat or the repo.

## 1. Google Cloud project

1. Go to https://console.cloud.google.com and open the project that has your Business Profile API access (the one
   Google approved). If you do not have one, create a project and request access at
   https://developers.google.com/my-business/content/prereqs (approval can take a few days).
2. **APIs & Services → Library**: enable **My Business Account Management API**, **My Business Business
   Information API** and **Google My Business API** (the reviews API lives here).

## 2. OAuth consent screen

1. **APIs & Services → OAuth consent screen** (or **Google Auth Platform → Branding / Audience**).
2. User type **External**; app name e.g. "Be Carrot Reviews"; support email; save.
3. **Data access / Scopes**: add `https://www.googleapis.com/auth/business.manage`.
4. **Audience**: click **Publish app** so it is **In production**. Leave it unverified; that is fine for your own
   account. (In "Testing" mode Google expires refresh tokens after 7 days, which would break the weekly pull.)

## 3. OAuth client

1. **APIs & Services → Credentials → Create credentials → OAuth client ID**.
2. Application type **Web application**; name "Reviews".
3. **Authorised redirect URIs**: add `https://developers.google.com/oauthplayground`
4. Create, and keep the **Client ID** and **Client secret** open in that window.

## 4. Get the refresh token (OAuth Playground)

1. Open https://developers.google.com/oauthplayground
2. Click the gear icon (top right), tick **Use your own OAuth credentials**, paste the Client ID and Client secret.
3. In "Step 1", type `https://www.googleapis.com/auth/business.manage` in the box and click **Authorize APIs**.
4. Sign in with the account that manages the Business Profiles; on the "Google hasn't verified this app" screen click
   **Advanced → Go to ... (unsafe)**, then **Allow**.
5. In "Step 2", click **Exchange authorization code for tokens**. Copy the **Refresh token**.

## 5. Save the three values

claude.ai/code → environment **BC Social Automation → Edit → Environment variables**, add:

```
GBP_CLIENT_ID=<client id>
GBP_CLIENT_SECRET=<client secret>
GBP_REFRESH_TOKEN=<refresh token>
```

Save, start a new session, and say **"check reviews"**. Claude runs `python scripts/gbp_reviews.py check`, which lists
every location the account can see and which client each maps to.
