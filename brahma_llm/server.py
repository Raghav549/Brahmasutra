"""🕉️ ब्रह्म-LLM सर्वर — the model *is* the application.

There is no app builder in this package.  You do not generate another program
that you then have to run; you run ब्रह्म, and it chats, writes सूत्र code,
executes code, explains code and renders images on the same dependency-free
HTTP server (:mod:`brahma_web`, stdlib only).

======================  ==================================================================
endpoint                what it really does
======================  ==================================================================
``GET  /``              one-page UI (chat · code · run · image)
``GET  /status``        model, kernel, corpus and last mission — all measured
``GET  /kernel``        boots the installed सूत्र-OS image and reports its output
``POST /chat``          ``{"message": "…"}`` → the agent runs the right capability
``POST /generate``      raw model continuation for a prompt
``POST /run``           compile + execute सूत्र source on the VM
``POST /explain``       structural analysis of सूत्र source
``GET  /image``         ``?prompt=…`` → a real PNG (model-driven procedural render)
``POST /train``         one autonomous training round (opt-in, off by default)
======================  ==================================================================

Safety: every program runs on the project's own VM with a step and depth budget;
nothing here shells out, and ``/train`` is disabled unless ``allow_train=True``.
"""

from __future__ import annotations

import os
from typing import Optional

from brahma_web import App, BadRequest, Response, json_response

from .agent import BrahmaAgent

INDEX_HTML = """<!doctype html>
<html lang="hi">
<head>
<meta charset="utf-8">
<title>🕉️ ब्रह्म-LLM</title>
<style>
 body { font-family: system-ui, sans-serif; margin: 2rem auto; max-width: 52rem; line-height: 1.55; }
 textarea, input { width: 100%; font-size: 1rem; font-family: inherit; padding: .5rem; }
 pre { background: #111; color: #eee; padding: 1rem; border-radius: 8px; overflow-x: auto; white-space: pre-wrap; }
 button { font-size: 1rem; padding: .5rem 1rem; border-radius: 6px; margin-right: .4rem; }
 .muted { color: #666; font-size: .9rem; }
 img { max-width: 100%; border-radius: 8px; border: 1px solid #333; }
</style>
</head>
<body>
<h1>🕉️ ब्रह्म-LLM</h1>
<p class="muted">मॉडल ही अनुप्रयोग है: बातचीत, सूत्र कोड, निष्पादन,
विश्लेषण और चित्र — एक ही सर्वर पर।</p>
<textarea id="message" rows="4"
  placeholder="कोड लिखो: अभाज्य संख्या जाँच / दर्शय 2 + 3 / चित्र बनाओ: शांति / status"></textarea>
<div>
  <button id="send">भेजें</button>
  <button id="status">स्थिति</button>
  <button id="kernel">कर्नेल</button>
</div>
<h2>उत्तर</h2>
<pre id="out">—</pre>
<h2>चित्र</h2>
<div id="picture" class="muted">अभी कोई चित्र नहीं</div>
<script>
const out = document.getElementById('out');
async function post(path, payload) {
  const response = await fetch(path, {method: 'POST', headers: {'Content-Type': 'application/json'},
                                      body: JSON.stringify(payload)});
  return await response.json();
}
async function get(path) { return await (await fetch(path)).json(); }

document.getElementById('send').onclick = async () => {
  const message = document.getElementById('message').value;
  out.textContent = 'सोच रहा है…';
  try {
    const data = await post('/chat', {message});
    out.textContent = data.text || JSON.stringify(data, null, 1);
    if (data.intent === 'image' && data.path) {
      const name = data.path.split('/').pop();
      const prompt = encodeURIComponent(data.prompt || message);
      document.getElementById('picture').innerHTML =
        '<img alt="' + name + '" src="/image?prompt=' + prompt + '">';
    }
  } catch (error) { out.textContent = 'त्रुटि: ' + error; }
};
document.getElementById('status').onclick = async () => {
  const data = await get('/status');
  out.textContent = JSON.stringify(data, null, 1);
};
document.getElementById('kernel').onclick = async () => {
  const data = await get('/kernel');
  out.textContent = JSON.stringify(data, null, 1);
};
</script>
</body>
</html>
"""


def create_app(model=None, checkpoint: Optional[str] = None, image_dir: Optional[str] = None,
               allow_train: bool = False, name: str = "🕉️ ब्रह्म-LLM") -> App:
    """Build the LLM application (no socket is opened here)."""
    agent = BrahmaAgent(model=model, checkpoint=checkpoint)
    pictures = image_dir or os.path.join(os.getcwd(), "chitra")
    os.makedirs(pictures, exist_ok=True)
    app = App(name)

    @app.route("/")
    def index(_request):
        return Response(status=200, payload=INDEX_HTML,
                        content_type="text/html; charset=utf-8")

    @app.route("/status")
    def status(_request):
        return json_response(agent.status())

    @app.route("/kernel")
    def kernel(_request):
        from .kernel import verify

        report = verify()
        return json_response({"ok": report["ok"], "steps": report["steps"],
                              "image_bytes": report["image_bytes"],
                              "output": report["output"], "problems": report["problems"]})

    @app.route("/chat", methods=("POST",))
    def chat(request):
        body = request.json()
        message = body.get("message", body.get("prompt"))
        if not isinstance(message, str) or not message.strip():
            raise BadRequest("message is required")
        if len(message) > 8000:
            raise BadRequest("message too long (max 8000 characters)")
        return json_response(agent.respond(message))

    @app.route("/generate", methods=("POST",))
    def generate(request):
        if agent.model is None:
            return json_response({"status": "unavailable",
                                  "reason": "कोई चेकपॉइंट नहीं"}, status=503)
        body = request.json()
        prompt = body.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            raise BadRequest("prompt is required")
        tokens = body.get("tokens", 60)
        temperature = body.get("temperature", 0.9)
        if not isinstance(tokens, int) or not 1 <= tokens <= 400:
            raise BadRequest("tokens must be an integer in 1..400")
        if not isinstance(temperature, (int, float)) or not 0.0 <= float(temperature) <= 2.0:
            raise BadRequest("temperature must be in 0..2")
        text = agent.model.generate(prompt, max_tokens=tokens, temperature=float(temperature))
        return json_response({"status": "ok", "text": text,
                              "params": agent.model.model.parameter_count()})

    @app.route("/run", methods=("POST",))
    def run(request):
        from brahma.api import execute

        body = request.json()
        source = body.get("source")
        if not isinstance(source, str) or not source.strip():
            raise BadRequest("source is required")
        if len(source) > 20_000:
            raise BadRequest("source too long (max 20000 characters)")
        report = execute(source, source_name="<http>", step_limit=200_000)
        return json_response({"ok": report.error is None, "output": report.output,
                              "error": None if report.error is None else str(report.error),
                              "steps": report.steps,
                              "elapsed": round(report.elapsed, 6)})

    @app.route("/explain", methods=("POST",))
    def explain(request):
        from .agent import explain as analyse

        body = request.json()
        source = body.get("source")
        if not isinstance(source, str) or not source.strip():
            raise BadRequest("source is required")
        return json_response(analyse(source))

    @app.route("/image")
    def image(request):
        prompt = request.query.get("prompt", "").strip()
        if not prompt:
            raise BadRequest("prompt query parameter is required")
        if len(prompt) > 500:
            raise BadRequest("prompt too long (max 500 characters)")
        target = os.path.join(pictures, "brahma-image.png")
        meta = agent.image(prompt, path=target)
        with open(target, "rb") as handle:
            blob = handle.read()
        return Response(status=200, payload=blob, content_type="image/png",
                        headers={"Cache-Control": "no-store",
                                 "X-Brahma-Origin": str(meta.get("origin", "")).split(":")[0],
                                 "X-Brahma-Seed": str(meta["seed"])})

    @app.route("/train", methods=("POST",))
    def train(request):
        if not allow_train:
            return json_response({"status": "disabled",
                                  "reason": "सर्वर पर प्रशिक्षण बंद है (allow_train=False)"},
                                 status=403)
        from .trainer import AutonomousTrainer, Target

        body = request.json()
        goal = body.get("target", "सूत्र में वैध कार्यक्रम लिखना सीखो")
        iterations = int(body.get("iterations", 1))
        trainer = AutonomousTrainer(log=lambda message: None)
        report = trainer.run(Target(description=goal, iterations=max(1, min(5, iterations)),
                                    epochs=1, budget_seconds=120))
        return json_response({"status": "ok", "best": report["best"],
                              "programs": report["programs"]})

    return app


def main(argv=None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="🕉️ ब्रह्म-LLM सर्वर")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--model", default=None, help="चेकपॉइंट निर्देशिका")
    parser.add_argument("--image-dir", default=None)
    parser.add_argument("--allow-train", action="store_true")
    parser.add_argument("--once", action="store_true", help="पोर्ट बाँधकर तुरंत बंद करें")
    args = parser.parse_args(argv)

    app = create_app(checkpoint=args.model, image_dir=args.image_dir,
                     allow_train=args.allow_train)
    if args.once:
        bound = app.start("127.0.0.1", args.port)
        app.shutdown()
        print("🕉️ ब्रह्म-LLM पोर्ट %d पर तैयार" % bound)
        return 0
    print("🕉️ ब्रह्म-LLM — http://%s:%d" % (args.host, args.port))
    app.serve(args.host, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
