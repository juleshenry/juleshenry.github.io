---
layout: post
title: "touch_keeper"
date: 2026-05-04
---

# [touch_keeper: Mass-Personalized New Year's Texts via Twilio](https://github.com/juleshenry/touch_keeper)

New Year's Eve. 11:58 PM. You want to text "Happy New Year" to everyone in your contacts. All 200+ of them. Personalized by name. Before midnight.

You could type fast. Or you could automate it.

touch_keeper is a Python CLI tool that parses your phone contacts (VCF file), sends a personalized SMS to each contact via the Twilio API, runs a webhook server that auto-replies when people text back, and then analyzes the response data with matplotlib visualizations.

The project is on [GitHub](https://github.com/juleshenry/touch_keeper). Apache 2.0 licensed.

## The Three Stages

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
