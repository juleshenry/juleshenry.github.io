---
layout: post
title: "touch_keeper: Mass-Personalized New Year's Texts via Twilio"
date: 2026-05-04
---

[View on GitHub](https://github.com/juleshenry/touch_keeper)

New Year's Eve. 11:58 PM. You want to text "Happy New Year" to everyone in your contacts. All 200+ of them. Personalized by name. Before midnight.

You could type fast. Or you could automate it.

touch_keeper is a Python CLI tool that parses your phone contacts (VCF file), sends a personalized SMS to each contact via the Twilio API, runs a webhook server that auto-replies when people text back, and then analyzes the response data with matplotlib visualizations.

The project is on [GitHub](https://github.com/juleshenry/touchkeeper). Apache 2.0 licensed.

<div id="nye-viz" style="width: 100%; height: 350px; margin: 2em 0; border-radius: 8px; overflow: hidden; background: #020617;"></div>

<script>
(function() {
  function initNYE() {
    if (typeof THREE === 'undefined') { setTimeout(initNYE, 100); return; }
    const container = document.getElementById('nye-viz');
    if (!container) return;
    const w = container.clientWidth, h = 350;
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x020617);
    const camera = new THREE.PerspectiveCamera(60, w / h, 0.1, 100);
    camera.position.set(0, 0, 20);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(w, h);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // Central phone
    const phoneGeo = new THREE.BoxGeometry(1.2, 2.2, 0.15);
    const phoneMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.8, roughness: 0.2 });
    const phone = new THREE.Mesh(phoneGeo, phoneMat);
    scene.add(phone);
    // Screen
    const screenGeo = new THREE.PlaneGeometry(1.0, 1.8);
    const screenMat = new THREE.MeshStandardMaterial({ color: 0x22d3ee, emissive: 0x22d3ee, emissiveIntensity: 0.3 });
    const screen = new THREE.Mesh(screenGeo, screenMat);
    screen.position.z = 0.08;
    phone.add(screen);

    // Message particles radiating outward
    const msgs = [];
    const msgColors = [0x22d3ee, 0x6366f1, 0xec4899, 0xf59e0b, 0x10b981, 0xa78bfa, 0xfbbf24, 0x34d399];
    for (let i = 0; i < 60; i++) {
      const geo = new THREE.SphereGeometry(0.08 + Math.random() * 0.08, 8, 8);
      const mat = new THREE.MeshStandardMaterial({ color: msgColors[i % msgColors.length], emissive: msgColors[i % msgColors.length], emissiveIntensity: 0.5 });
      const m = new THREE.Mesh(geo, mat);
      const angle = Math.random() * Math.PI * 2;
      const speed = 1.5 + Math.random() * 3;
      const ySpeed = (Math.random() - 0.5) * 2;
      m._vx = Math.cos(angle) * speed;
      m._vy = ySpeed;
      m._vz = Math.sin(angle) * speed * 0.3;
      m._life = Math.random() * 3;
      m._maxLife = 2.5 + Math.random() * 1.5;
      m.position.set(0, 0, 0);
      scene.add(m);
      msgs.push(m);
    }

    scene.add(new THREE.AmbientLight(0xffffff, 0.4));
    const pl = new THREE.PointLight(0x22d3ee, 1.5, 20);
    pl.position.set(0, 0, 5);
    scene.add(pl);

    function animate() {
      requestAnimationFrame(animate);
      const dt = 0.016;
      const t = Date.now() * 0.001;
      phone.rotation.y = Math.sin(t * 0.3) * 0.15;
      phone.rotation.x = Math.sin(t * 0.2) * 0.05;
      screenMat.emissiveIntensity = 0.2 + Math.sin(t * 2) * 0.15;
      for (const m of msgs) {
        m._life += dt;
        if (m._life > m._maxLife) {
          m._life = 0;
          m.position.set(0, 0, 0);
          const angle = Math.random() * Math.PI * 2;
          const speed = 1.5 + Math.random() * 3;
          m._vx = Math.cos(angle) * speed;
          m._vy = (Math.random() - 0.5) * 2;
          m._vz = Math.sin(angle) * speed * 0.3;
        }
        m.position.x += m._vx * dt;
        m.position.y += m._vy * dt;
        m.position.z += m._vz * dt;
        const fade = 1 - (m._life / m._maxLife);
        m.material.opacity = fade;
        m.material.transparent = true;
        m.scale.setScalar(fade);
      }
      renderer.render(scene, camera);
    }
    window.addEventListener('resize', function() {
      const nw = container.clientWidth;
      camera.aspect = nw / h;
      camera.updateProjectionMatrix();
      renderer.setSize(nw, h);
    });
    animate();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initNYE);
  else initNYE();
})();
</script>
<p style="text-align:center; color:#64748b; font-size:0.85em; margin-top:-1em;">200+ personalized SMS messages radiating out at midnight.</p>

## The Three Stages

<svg viewBox="0 0 700 110" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:700px;display:block;margin:1.5em auto;">
  <rect width="700" height="110" rx="8" fill="#0f172a"/>
  <!-- Stage 1: Send -->
  <rect x="20" y="20" width="180" height="70" rx="10" fill="#0c2d48" stroke="#22d3ee" stroke-width="2"/>
  <text x="110" y="48" text-anchor="middle" fill="#22d3ee" font-size="14" font-weight="bold" font-family="monospace">1. SEND</text>
  <text x="110" y="68" text-anchor="middle" fill="#64748b" font-size="10" font-family="monospace">VCF -> Twilio SMS</text>
  <text x="110" y="80" text-anchor="middle" fill="#475569" font-size="9" font-family="monospace">200+ personalized texts</text>
  <!-- Arrow -->
  <polygon points="210,55 225,48 225,52 250,52 250,58 225,58 225,62" fill="#fbbf24"/>
  <!-- Stage 2: Serve -->
  <rect x="255" y="20" width="180" height="70" rx="10" fill="#2d1a0a" stroke="#f59e0b" stroke-width="2"/>
  <text x="345" y="48" text-anchor="middle" fill="#fbbf24" font-size="14" font-weight="bold" font-family="monospace">2. SERVE</text>
  <text x="345" y="68" text-anchor="middle" fill="#64748b" font-size="10" font-family="monospace">Flask webhook /sms</text>
  <text x="345" y="80" text-anchor="middle" fill="#475569" font-size="9" font-family="monospace">Auto-reply + logging</text>
  <!-- Arrow -->
  <polygon points="445,55 460,48 460,52 485,52 485,58 460,58 460,62" fill="#fbbf24"/>
  <!-- Stage 3: Analyze -->
  <rect x="490" y="20" width="190" height="70" rx="10" fill="#1a0c2d" stroke="#a855f7" stroke-width="2"/>
  <text x="585" y="48" text-anchor="middle" fill="#c084fc" font-size="14" font-weight="bold" font-family="monospace">3. ANALYZE</text>
  <text x="585" y="68" text-anchor="middle" fill="#64748b" font-size="10" font-family="monospace">response.log -> charts</text>
  <text x="585" y="80" text-anchor="middle" fill="#475569" font-size="9" font-family="monospace">173 replies visualized</text>
</svg>

### 1. Send

```bash
touch-keeper send --contacts contacts.vcf --sender "Jules"
```

Parses the VCF file, extracts names and phone numbers, normalizes numbers to E.164 format (handling the chaos of inconsistent phone number formatting -- parentheses, dashes, spaces, country codes, no country codes), and fires off a personalized SMS to each contact via the Twilio API:

> Happy New Year, Maria!!! (~‾⌣‾)~
> Cheers, Jules

Messages are spaced with a configurable delay (default 1 second) to avoid hitting Twilio's rate limits. A dry-run mode previews all messages without sending.

### 2. Serve

```bash
touch-keeper serve
```

Launches a Flask webhook server at `/sms`. When Twilio receives a reply from one of your contacts, it forwards the message to your webhook. The server handles replies differently based on whether the person has replied before:

- **First-time replier**: Gets a warm, personal-sounding response: *"May the new decade find you great happiness and prosperity."*
- **Repeat replier**: Gets a random celebration emoji from a curated set -- party poppers, champagne glasses, fireworks, confetti balls.

All incoming messages are logged to `response.log` with the sender's phone number and timestamp.

The auto-reply is the part that creates the most entertainment. People think they are texting a person. They are texting a Flask server. The responses are just plausible enough to sustain a back-and-forth for 2-3 messages before suspicion sets in.

### 3. Analyze

```bash
touch-keeper analyze --contacts contacts.vcf --log response.log
```

Reads the response log, maps phone numbers back to contact names using the VCF file, and generates:

- A text summary of all replies per contact
- A bar chart histogram of response frequency (sorted descending -- who replied the most?)
- A time-series scatter plot of when replies came in, with quartile lines showing the distribution of reply times

## The Response Log: A Time Capsule

<svg viewBox="0 0 500 140" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:500px;display:block;margin:1.5em auto;">
  <rect width="500" height="140" rx="8" fill="#0f172a"/>
  <text x="250" y="22" text-anchor="middle" fill="#64748b" font-size="11" font-family="monospace">NYE 2019/2020 Response Stats</text>
  <!-- Bar: sent -->
  <rect x="40" y="35" width="400" height="28" rx="5" fill="#1e293b"/>
  <rect x="40" y="35" width="400" height="28" rx="5" fill="#22d3ee" opacity="0.7"/>
  <text x="250" y="54" text-anchor="middle" fill="#0f172a" font-size="12" font-weight="bold" font-family="monospace">200+ sent</text>
  <!-- Bar: replied -->
  <rect x="40" y="70" width="346" height="28" rx="5" fill="#1e293b"/>
  <rect x="40" y="70" width="346" height="28" rx="5" fill="#10b981" opacity="0.7"/>
  <text x="213" y="89" text-anchor="middle" fill="#0f172a" font-size="12" font-weight="bold" font-family="monospace">173 replied (86.5%)</text>
  <!-- Bar: reconnections -->
  <rect x="40" y="105" width="60" height="28" rx="5" fill="#1e293b"/>
  <rect x="40" y="105" width="60" height="28" rx="5" fill="#f59e0b" opacity="0.7"/>
  <text x="130" y="124" fill="#fbbf24" font-size="11" font-family="monospace">real meetups after</text>
</svg>

The included `response.log` contains **173 real replies** from what appears to be a New Year's Eve 2019/2020 deployment. I am going to quote some of these because they are a genuine cross-section of human reaction to receiving an automated-but-personalized text at midnight:

The grateful:
> *"Love you juju"*

The suspicious:
> *"Is this some auto response shit"*

The testing:
> *"Did you get a new phone??"*

The wholesome:
> *"Happy New Year!! Miss you man"*

The pragmatic:
> *"Coffee or a drink... or a blunt whatever works"*

The recursive:
> Someone figured out the auto-reply and kept texting to see how many different emojis they could get.

173 replies out of ~200 contacts is a remarkable response rate. Turns out, people appreciate being remembered at midnight even if the remembering was automated. The personalization (including their name) makes each message feel intentional, and the auto-reply sustains the illusion just long enough for the warmth to land.

## Technical Notes

The codebase is clean modern Python. Frozen dataclasses for immutable data models (`Contact`, `Settings`). Type annotations throughout. Strict mypy. ruff for linting. pytest for testing. `src/` layout convention. `pyproject.toml` with Hatchling build system.

The VCF parser handles the various vCard format quirks -- multiple phone numbers per contact (picks the first mobile number), names stored as "Last;First" or "First Last", phone numbers with `tel:` URI prefixes. Phone number normalization to E.164 strips all formatting characters and prepends the country code if missing.

The analysis module uses pandas for data manipulation and matplotlib for the visualizations. The quartile lines on the time-series plot are a nice touch -- they show that most replies cluster in the first 30 minutes after midnight, with a long tail of late-night stragglers responding hours later.

## Why Twilio?

Twilio is the path of least resistance for programmatic SMS. The Python SDK (`twilio>=9.0`) wraps the REST API cleanly, and the webhook integration with Flask is trivial -- Twilio sends a POST request to your `/sms` endpoint with the sender's number and message body. You respond with TwiML (Twilio Markup Language), which is XML that specifies the reply message. It is not elegant, but it works, and you can have the whole thing running in 20 lines of Flask.

The cost is roughly $0.0075 per SMS in the US. 200 contacts costs about $1.50 in Twilio credits. A dollar fifty to text your entire phone book a personalized New Year's message. That is cheaper than a greeting card.

## The Philosophical Bit

There is something slightly absurd about automating personal connection. The whole point of a New Year's text is that someone thought of you. If a script thought of you, does it count?

I think it does, actually. The automation handles the logistics -- the typing, the timing, the 200 repetitions of the same sentiment. But the decision to send the text was human. The contact list was curated by a human over years of real relationships. The message template was written by a human who wanted those specific people to feel remembered. The automation scales the intention without diluting it.

173 people replied. Several led to actual meetups in the following weeks. One person I had not spoken to in three years texted back and we reconnected. The script did not create the connection. It removed the friction that was preventing it.

Keep in touch.
