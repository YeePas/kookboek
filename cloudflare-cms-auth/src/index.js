const GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize";
const GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token";
const STATE_COOKIE = "decap_oauth_state";

function html(status, content) {
  const payload = encodeURIComponent(JSON.stringify(content));
  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>CMS auth</title>
  </head>
  <body>
    <script>
      (function() {
        const receiveMessage = (message) => {
          window.opener.postMessage(
            'authorization:github:${status}:' + decodeURIComponent('${payload}'),
            message.origin
          );
          window.removeEventListener('message', receiveMessage, false);
          window.close();
        };
        window.addEventListener('message', receiveMessage, false);
        window.opener.postMessage('authorizing:github', '*');
      })();
    </script>
  </body>
</html>`;
}

function withSecurityHeaders(headers = new Headers(), contentType = "text/plain; charset=UTF-8") {
  headers.set("content-type", contentType);
  headers.set("x-content-type-options", "nosniff");
  headers.set("referrer-policy", "strict-origin-when-cross-origin");
  headers.set("cache-control", "no-store");
  headers.set("content-security-policy", "default-src 'none'; script-src 'unsafe-inline'; connect-src 'none'; img-src 'none'; style-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'");
  return headers;
}

function getCookie(request, name) {
  const cookie = request.headers.get("Cookie") || "";
  const match = cookie.match(new RegExp(`(?:^|; )${name}=([^;]+)`));
  return match ? decodeURIComponent(match[1]) : null;
}

function randomState() {
  const bytes = crypto.getRandomValues(new Uint8Array(18));
  return Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
}

function redirect(url, cookie) {
  const headers = new Headers({ Location: url.toString() });
  if (cookie) headers.append("Set-Cookie", cookie);
  return new Response(null, { status: 302, headers });
}

async function handleAuth(request, env) {
  if (!env.GITHUB_OAUTH_ID) {
    return new Response("Missing GITHUB_OAUTH_ID secret", { status: 500 });
  }

  const url = new URL(request.url);
  const state = randomState();
  const scope = env.GITHUB_SCOPE || "public_repo read:user";
  const redirectUri = `${url.origin}/callback`;
  const authorizeUrl = new URL(GITHUB_AUTHORIZE_URL);
  authorizeUrl.searchParams.set("client_id", env.GITHUB_OAUTH_ID);
  authorizeUrl.searchParams.set("redirect_uri", redirectUri);
  authorizeUrl.searchParams.set("scope", scope);
  authorizeUrl.searchParams.set("state", state);

  const cookie = `${STATE_COOKIE}=${encodeURIComponent(state)}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=600`;
  return redirect(authorizeUrl, cookie);
}

async function exchangeCodeForToken(request, env) {
  if (!env.GITHUB_OAUTH_ID || !env.GITHUB_OAUTH_SECRET) {
    return new Response("Missing GitHub OAuth secrets", { status: 500 });
  }

  const url = new URL(request.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  const cookieState = getCookie(request, STATE_COOKIE);

  if (!code) {
    return new Response(html("error", { error: "Missing code" }), {
      status: 400,
      headers: withSecurityHeaders(new Headers(), "text/html; charset=UTF-8"),
    });
  }

  if (!state || !cookieState || state !== cookieState) {
    return new Response(html("error", { error: "Invalid state" }), {
      status: 401,
      headers: withSecurityHeaders(new Headers({
        "Set-Cookie": `${STATE_COOKIE}=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0`,
      }), "text/html; charset=UTF-8"),
    });
  }

  const response = await fetch(GITHUB_TOKEN_URL, {
    method: "POST",
    headers: {
      accept: "application/json",
      "content-type": "application/json",
      "user-agent": "foodnotes-cms-auth",
    },
    body: JSON.stringify({
      client_id: env.GITHUB_OAUTH_ID,
      client_secret: env.GITHUB_OAUTH_SECRET,
      code,
      redirect_uri: `${url.origin}/callback`,
    }),
  });

  const data = await response.json();
  if (!response.ok || data.error) {
    return new Response(html("error", data), {
      status: 401,
      headers: withSecurityHeaders(new Headers({
        "Set-Cookie": `${STATE_COOKIE}=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0`,
      }), "text/html; charset=UTF-8"),
    });
  }

  if (env.ALLOWED_GITHUB_USERS) {
    const allowedUsers = String(env.ALLOWED_GITHUB_USERS)
      .split(",")
      .map((user) => user.trim().toLowerCase())
      .filter(Boolean);

    if (allowedUsers.length > 0) {
      const userResponse = await fetch("https://api.github.com/user", {
        headers: {
          authorization: `Bearer ${data.access_token}`,
          accept: "application/vnd.github+json",
          "user-agent": "foodnotes-cms-auth",
        },
      });

      if (!userResponse.ok) {
        return new Response(html("error", { error: "Unable to verify GitHub user" }), {
          status: 401,
          headers: withSecurityHeaders(new Headers({
            "Set-Cookie": `${STATE_COOKIE}=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0`,
          }), "text/html; charset=UTF-8"),
        });
      }

      const userData = await userResponse.json();
      const login = String(userData.login || "").toLowerCase();
      if (!allowedUsers.includes(login)) {
        return new Response(html("error", { error: "GitHub user is not allowed" }), {
          status: 403,
          headers: withSecurityHeaders(new Headers({
            "Set-Cookie": `${STATE_COOKIE}=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0`,
          }), "text/html; charset=UTF-8"),
        });
      }
    }
  }

  return new Response(
    html("success", { token: data.access_token, provider: "github" }),
    {
      status: 200,
      headers: withSecurityHeaders(new Headers({
        "Set-Cookie": `${STATE_COOKIE}=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0`,
      }), "text/html; charset=UTF-8"),
    }
  );
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/auth") {
      return handleAuth(request, env);
    }

    if (url.pathname === "/callback") {
      return exchangeCodeForToken(request, env);
    }

    return new Response("Hello from the Foodnotes CMS auth worker.", {
      headers: withSecurityHeaders(),
    });
  },
};
