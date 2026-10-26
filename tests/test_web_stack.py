"""Tests for the dependency-free web stack and the demo builders.

These modules replaced an undeclared Flask dependency, so they are tested like
any other engine module: routing, JSON handling, authentication, path safety and
the code generators that emit self-contained applications.
"""

from __future__ import annotations

import json
import os
import sys
import threading
import urllib.error
import urllib.request

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import brahma_auto  # noqa: E402  (path setup must happen first)
import brahma_bytecode  # noqa: E402
import brahma_cli  # noqa: E402
import brahma_chat  # noqa: E402
import brahma_paths  # noqa: E402
import brahma_templates  # noqa: E402
from brahma_web import App, BadRequest, Request, Response  # noqa: E402


def get(app, path, **kwargs):
    return app.handle(Request(method="GET", path=path, **kwargs))


def post(app, path, body=None, token=None):
    headers = {"token": token} if token else {}
    return app.handle(Request(method="POST", path=path, headers=headers, body=body or {}))


# ---------------------------------------------------------------------------
# brahma_web
# ---------------------------------------------------------------------------
class TestApp:
    def test_routes_and_dict_payload(self):
        app = App("test")

        @app.route("/status")
        def status(request):
            return {"status": "ok", "path": request.path}

        response = get(app, "/status")
        assert isinstance(response, Response)
        assert response.status == 200
        assert response.payload == {"status": "ok", "path": "/status"}
        assert "application/json" in response.content_type

    def test_unknown_route_is_404(self):
        response = get(App(), "/nope")
        assert response.status == 404
        assert response.payload["status"] == "error"

    def test_method_not_allowed_is_405(self):
        app = App()

        @app.route("/only-post", methods=("POST",))
        def only_post(request):
            return {"ok": True}

        response = get(app, "/only-post")
        assert response.status == 405
        assert response.payload["allowed"] == ["POST"]

    def test_path_parameters(self):
        app = App()

        @app.route("/greet/{name}")
        def greet(request, name):
            return {"hello": name}

        assert get(app, "/greet/ram").payload == {"hello": "ram"}

    def test_trailing_slash_is_ignored(self):
        app = App()
        app.route("/x")(lambda request: {"ok": 1})
        assert get(app, "/x/").status == 200

    def test_missing_field_is_400(self):
        app = App()

        @app.route("/needs", methods=("POST",))
        def needs(request):
            return {"value": request.json()["required"]}

        response = post(app, "/needs", {"other": 1})
        assert response.status == 400
        assert "required" in response.payload["message"]

    def test_bad_request_exception(self):
        app = App()

        @app.route("/bad")
        def bad(request):
            raise BadRequest("no good")

        response = get(app, "/bad")
        assert response.status == 400
        assert response.payload["message"] == "no good"

    def test_internal_error_does_not_leak_traceback(self):
        app = App()

        @app.route("/boom")
        def boom(request):
            raise RuntimeError("secret detail")

        response = get(app, "/boom")
        assert response.status == 500
        assert "Traceback" not in json.dumps(response.payload)

    def test_text_and_custom_response(self):
        app = App()
        app.route("/text")(lambda request: "plain")
        app.route("/custom")(lambda request: Response(status=201, payload={"created": True}))

        text = get(app, "/text")
        assert text.content_type.startswith("text/plain")
        assert get(app, "/custom").status == 201

    def test_request_parsing(self):
        request = Request.parse(
            "post", "/a/b?x=1&y=2", {"Token": "abc"}, b'{"k": "v"}'
        )
        assert request.method == "POST"
        assert request.path == "/a/b"
        assert request.query == {"x": "1", "y": "2"}
        assert request.header("token") == "abc"
        assert request.json() == {"k": "v"}

    def test_invalid_json_raises_bad_request(self):
        request = Request.parse("POST", "/", {}, b"not json")
        with pytest.raises(BadRequest):
            request.json()

    def test_real_http_roundtrip(self):
        app = App("http-test")
        app.route("/status")(lambda request: {"status": "RUNNING"})
        port = app.start("127.0.0.1", 0)
        try:
            with urllib.request.urlopen("http://127.0.0.1:%d/status" % port, timeout=10) as handle:
                assert json.load(handle)["status"] == "RUNNING"
        finally:
            app.shutdown()

    def test_cors_header_is_sent(self):
        app = App()
        app.route("/x")(lambda request: {"ok": True})
        port = app.start("127.0.0.1", 0)
        try:
            with urllib.request.urlopen("http://127.0.0.1:%d/x" % port, timeout=10) as handle:
                assert handle.headers["Access-Control-Allow-Origin"] == "*"
        finally:
            app.shutdown()


# ---------------------------------------------------------------------------
# brahma_chat
# ---------------------------------------------------------------------------
class TestChat:
    @pytest.fixture()
    def app(self, tmp_path):
        return brahma_chat.create_app("test-chat", data_dir=str(tmp_path), admin=True,
                                      admin_password="s3cret")

    def register(self, app, username="ram", password="pw"):
        return post(app, "/register", {"username": username, "password": password})

    def login(self, app, username="ram", password="pw"):
        return post(app, "/login", {"username": username, "password": password}).payload["token"]

    def test_status(self, app):
        assert get(app, "/status").payload["status"] == "RUNNING"

    def test_register_login_flow(self, app):
        assert self.register(app).payload["status"] == "ok"
        assert self.register(app).payload["status"] == "exists"
        assert post(app, "/login", {"username": "ram", "password": "bad"}).payload["status"] == "fail"
        token = self.login(app)
        assert get(app, "/dashboard", headers={"token": token}).payload["user"] == "ram"

    def test_passwords_are_hashed(self, app, tmp_path):
        self.register(app)
        stored = (tmp_path / "users.json").read_text(encoding="utf-8")
        assert "pw" not in stored
        record = json.loads(stored)["ram"]
        assert set(record) == {"salt", "hash"}
        assert len(record["hash"]) == 64

    def test_same_password_different_salt(self, tmp_path):
        store = brahma_chat.Store(str(tmp_path))
        store.add_user("a", "same")
        store.add_user("b", "same")
        users = store.users()
        assert users["a"]["salt"] != users["b"]["salt"]
        assert users["a"]["hash"] != users["b"]["hash"]
        assert store.check_password("a", "same")
        assert not store.check_password("a", "other")
        assert not store.check_password("missing", "same")

    def test_chat_requires_token(self, app):
        assert post(app, "/send", {"msg": "hi"}).status == 401
        token = self.login_after_register(app)
        assert post(app, "/send", {"msg": "नमस्ते"}, token=token).payload["status"] == "sent"
        messages = get(app, "/chat").payload["messages"]
        assert messages == [{"user": "ram", "msg": "नमस्ते"}]

    def test_send_requires_message(self, app):
        token = self.login_after_register(app)
        assert post(app, "/send", {}, token=token).status == 400

    def test_admin_endpoints(self, app):
        self.register(app)
        bad = post(app, "/admin_login", {"username": "admin", "password": "wrong"})
        assert bad.payload["status"] == "fail"

        ok = post(app, "/admin_login", {"username": "admin", "password": "s3cret"}).payload
        assert ok["status"] == "ok"
        admin = ok["token"]

        assert get(app, "/users", headers={"token": admin}).payload["users"] == ["ram"]
        assert post(app, "/delete_user", {"username": "ram"}, token=admin).payload["status"] == "deleted"
        assert get(app, "/users", headers={"token": admin}).payload["users"] == []

    def test_users_requires_admin(self, app):
        token = self.login_after_register(app)
        assert get(app, "/users", headers={"token": token}).status == 401

    def test_generated_admin_password_is_not_hardcoded(self, tmp_path):
        app = brahma_chat.create_app("x", data_dir=str(tmp_path), admin=True)
        assert getattr(app, "admin_password", "")
        assert getattr(app, "admin_password") != "admin123"

    def test_observer_cannot_bypass_validation(self, app):
        assert post(app, "/register", {"username": "x"}).status == 400
        assert post(app, "/register", {"username": 1, "password": "p"}).status == 400
        assert post(app, "/register", {"username": "u" * 500, "password": "p"}).status == 400

    def login_after_register(self, app):
        self.register(app)
        return self.login(app)


# ---------------------------------------------------------------------------
# brahma_bytecode + compilers
# ---------------------------------------------------------------------------
class TestBytecode:
    def test_assemble_and_run(self):
        code = brahma_bytecode.assemble("संकल्प अ 50\nसंकल्प ब 70\nयोग अ ब\nदर्शय अ")
        assert brahma_bytecode.run(code, verbose=False) == {"अ": 120, "ब": 70}

    def test_arithmetic_ops(self):
        code = brahma_bytecode.assemble(
            "संकल्प अ 10\nसंकल्प ब 4\nघटा अ ब\nगुण अ ब"
        )
        assert brahma_bytecode.run(code, verbose=False)["अ"] == 24

    def test_unknown_mnemonic_raises(self):
        with pytest.raises(brahma_bytecode.असेंबली_त्रुटि):
            brahma_bytecode.assemble("उड़ाओ x")

    def test_unknown_register_raises(self):
        with pytest.raises(brahma_bytecode.असेंबली_त्रुटि):
            brahma_bytecode.assemble("संकल्प झ 1")

    def test_truncated_instruction_raises(self):
        with pytest.raises(brahma_bytecode.असेंबली_त्रुटि):
            brahma_bytecode.run(b"\x01\x01", verbose=False)

    def test_unknown_opcode_raises(self):
        with pytest.raises(brahma_bytecode.असेंबली_त्रुटि):
            brahma_bytecode.run(b"\x7f", verbose=False)

    def test_disassemble_roundtrip(self):
        text = "संकल्प अ 50\nयोग अ ब\nदर्शय अ\nनिर्गम"
        listing = brahma_bytecode.disassemble(brahma_bytecode.assemble(text))
        assert listing.splitlines()[:3] == ["संकल्प अ 50", "योग अ ब", "दर्शय अ"]

    def test_halt_is_appended(self):
        code = brahma_bytecode.assemble("संकल्प अ 1")
        assert code[-1] == brahma_bytecode.HALT

    def test_image_pack_unpack(self):
        kernel = brahma_bytecode.assemble("संकल्प अ 7")
        image = brahma_bytecode.pack_image(kernel)
        assert image.startswith(brahma_bytecode.IMAGE_SIGNATURE)
        version, unpacked = brahma_bytecode.unpack_image(image)
        assert version == brahma_bytecode.IMAGE_VERSION
        assert unpacked == kernel

    def test_bad_image(self):
        with pytest.raises(brahma_bytecode.असेंबली_त्रुटि):
            brahma_bytecode.unpack_image(b"NOPE")
        with pytest.raises(brahma_bytecode.असेंबली_त्रुटि):
            brahma_bytecode.unpack_image(brahma_bytecode.pack_image(b"\x06")[:-1])

    def test_all_compilers_share_one_format(self, tmp_path):
        from सूत्र_संकलक import संकलक
        from सूत्र_मूल_संकलक import मूलसंकलक

        source = tmp_path / "p.sūtra"
        source.write_text("संकल्प अ 5\nदर्शय अ\n", encoding="utf-8")
        expected = brahma_bytecode.assemble(source.read_text(encoding="utf-8"))

        for index, compiler in enumerate((संकलक(), मूलसंकलक())):
            target = tmp_path / ("out%d.यन्त्र" % index)
            compiler.संकलन(str(source), str(target))
            assert target.read_bytes() == expected

        assert brahma_bytecode.run(expected, verbose=False) == {"अ": 5}

    def test_interpreter_accepts_both_apis(self):
        from सूत्र_यन्त्र_निष्पादक import सूत्रयन्त्र, यन्त्रनिष्पादक

        code = brahma_bytecode.assemble("संकल्प अ 3\nयोग अ अ")
        machine = यन्त्रनिष्पादक(verbose=False)
        assert machine.चलाओ(code)["अ"] == 6
        assert सूत्रयन्त्र(verbose=False).निष्पादन(code)["अ"] == 6


# ---------------------------------------------------------------------------
# brahma_paths / brahma_cli
# ---------------------------------------------------------------------------
class TestPathsAndCli:
    def test_data_root_uses_env(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BRAHMA_HOME", str(tmp_path))
        assert brahma_paths.data_root("ब्रह्म_AI_अनुप्रयोग") == str(tmp_path / "ब्रह्म_AI_अनुप्रयोग")

    def test_data_root_refuses_escape(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BRAHMA_HOME", str(tmp_path))
        with pytest.raises(ValueError):
            brahma_paths.data_root("..", "..", "etc")

    def test_ensure_dir(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BRAHMA_HOME", str(tmp_path))
        created = brahma_paths.ensure_dir(brahma_paths.data_root("apps"))
        assert os.path.isdir(created)

    def test_run_returns_codes(self):
        assert brahma_cli.run(lambda: None) == 0
        assert brahma_cli.run(lambda: 3) == 3
        assert brahma_cli.run(lambda argv: 0) == 0

    def test_run_handles_eof(self, capsys):
        def needs_input():
            raise EOFError()

        assert brahma_cli.run(needs_input) == 2
        assert "इनपुट" in capsys.readouterr().err

    def test_run_handles_keyboard_interrupt(self):
        def interrupted():
            raise KeyboardInterrupt()

        assert brahma_cli.run(interrupted) == 130

    def test_ask_returns_default_on_eof(self, monkeypatch):
        def boom(_prompt=""):
            raise EOFError()

        monkeypatch.setattr("builtins.input", boom)
        assert brahma_cli.पूछो("?", "डिफ़ॉल्ट") == "डिफ़ॉल्ट"

    def test_ask_propagates_eof_without_default(self, monkeypatch):
        def boom(_prompt=""):
            raise EOFError()

        monkeypatch.setattr("builtins.input", boom)
        with pytest.raises(EOFError):
            brahma_cli.पूछो("?")


# ---------------------------------------------------------------------------
# brahma_templates / brahma_auto
# ---------------------------------------------------------------------------
class TestGenerators:
    def test_written_servers_compile(self, tmp_path):
        chat = brahma_templates.write_chat_server(str(tmp_path / "chat"), "demo")
        api = brahma_templates.write_status_server(str(tmp_path / "api"), "demo")
        for path in (chat, api):
            source = open(path, encoding="utf-8").read()
            compile(source, path, "exec")
            assert "import flask" not in source.lower()

    def test_templates_are_stdlib_only(self):
        assert "ThreadingHTTPServer" in brahma_templates.CHAT_SERVER
        assert "from flask" not in brahma_templates.CHAT_SERVER
        assert "from flask" not in brahma_templates.STATUS_SERVER

    def test_safe_app_name(self):
        assert brahma_auto.safe_app_name("मेरा चैट ऐप") == "मेरा_चैट_ऐप"
        assert brahma_auto.safe_app_name("../../etc") == "etc"
        assert brahma_auto.safe_app_name("") == "brahma_app"
        assert "/" not in brahma_auto.safe_app_name("a/b")

    def test_create_app_writes_runnable_files(self, tmp_path):
        path = brahma_auto.create_app("डेमो चैट ऐप", base=str(tmp_path), port=0)
        assert os.path.isfile(os.path.join(path, "backend", "server.py"))
        assert os.path.isfile(os.path.join(path, "frontend", "index.html"))
        assert os.path.isfile(os.path.join(path, "README.md"))
        compile(open(os.path.join(path, "backend", "server.py"), encoding="utf-8").read(),
                "server.py", "exec")

    def test_dry_run_writes_nothing(self, tmp_path, capsys):
        path = brahma_auto.create_app("सूखा", base=str(tmp_path), dry_run=True)
        assert not os.path.exists(path)
        assert "बनाया जाएगा" in capsys.readouterr().out

    def test_main_requires_a_prompt(self, capsys):
        assert brahma_auto.main([]) == 2
        assert "विवरण" in capsys.readouterr().err

    def test_main_creates_app(self, tmp_path):
        assert brahma_auto.main(["प्रॉम्प्ट चैट ऐप", "--out", str(tmp_path), "--explain"]) == 0
        assert os.path.isdir(tmp_path / "प्रॉम्प्ट_चैट_ऐप")

    def test_legacy_names_point_here(self):
        import brahma_auto_v2

        assert brahma_auto_v2.create_app is brahma_auto.create_app


# ---------------------------------------------------------------------------
# demo backends (replaced Flask servers)
# ---------------------------------------------------------------------------
class TestDemoBackends:
    @pytest.mark.parametrize(
        "path,port,kind",
        [
            ("ब्रह्म_AI_अनुप्रयोग/chat_app/backend/server.py", 9000, "chat"),
            ("ब्रह्म_AI_अनुप्रयोग/chat_saas/backend/server.py", 9100, "chat"),
            ("ब्रह्म_AI_अनुप्रयोग/chat_admin_saas/backend/server.py", 9200, "admin"),
            ("ब्रह्म_स्थापित/chat_app_with_login_database_api_dashboard/backend/server.py", 9400, "chat"),
            ("ब्रह्म_AI_अनुप्रयोग/chat_app_with_login_database_api_dashboard/backend/api.py", 9310, "api"),
        ],
    )
    def test_backend_is_importable_and_stdlib_only(self, path, port, kind):
        full = os.path.join(REPO_ROOT, path)
        source = open(full, encoding="utf-8").read()
        assert "from flask" not in source, "Flask बैकएंड नहीं होना चाहिए"
        assert "--once" in source
        # importing must not open a socket
        namespace = {"__name__": "probe", "__file__": full}
        exec(compile(source, full, "exec"), namespace)
        expected_default = "chat_main" if kind != "api" else "create_app"
        assert expected_default in source

    def test_exec_api_refuses_traversal(self, tmp_path):
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "api_probe", os.path.join(REPO_ROOT, "ब्रह्म_API_स्वचालित_निष्पादन.py")
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        module.create_app(str(tmp_path))
        with pytest.raises(module.BadRequest):
            module.safe_app_path(str(tmp_path), "../../etc/passwd")
        with pytest.raises(module.BadRequest):
            module.safe_app_path(str(tmp_path), "missing.py")
        (tmp_path / "ok.py").write_text("print('hi')", encoding="utf-8")
        assert module.safe_app_path(str(tmp_path), "ok.py").endswith("ok.py")

    def test_exec_api_disabled_by_default(self, tmp_path, monkeypatch):
        import importlib.util

        monkeypatch.delenv("BRAHMA_ALLOW_EXEC", raising=False)
        spec = importlib.util.spec_from_file_location(
            "api_probe2", os.path.join(REPO_ROOT, "ब्रह्म_API_स्वचालित_निष्पादन.py")
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        (tmp_path / "ok.py").write_text("print('hi')", encoding="utf-8")
        app = module.create_app(str(tmp_path))
        response = post(app, "/run", {"app": "ok.py"})
        assert response.status == 400
        assert "disabled" in response.payload["message"]

    def test_exec_api_runs_in_subprocess(self, tmp_path, monkeypatch):
        import importlib.util

        monkeypatch.setenv("BRAHMA_ALLOW_EXEC", "1")
        spec = importlib.util.spec_from_file_location(
            "api_probe3", os.path.join(REPO_ROOT, "ब्रह्म_API_स्वचालित_निष्पादन.py")
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        (tmp_path / "ok.py").write_text("print('नमस्ते')", encoding="utf-8")
        app = module.create_app(str(tmp_path))
        response = post(app, "/run", {"app": "ok.py"})
        assert response.payload["status"] == "success"
        assert "नमस्ते" in response.payload["output"]


# ---------------------------------------------------------------------------
# no sockets / threads left behind
# ---------------------------------------------------------------------------
def test_no_lingering_threads():
    before = threading.active_count()
    app = App()
    app.route("/x")(lambda request: {"ok": True})
    port = app.start("127.0.0.1", 0)
    app.shutdown()
    assert port > 0
    assert threading.active_count() <= before


# ---------------------------------------------------------------------------
# brahma_ai (the one module that really is a model)
# ---------------------------------------------------------------------------
class TestAiModel:
    def make(self):
        import brahma_ai

        model = brahma_ai.MarkovModel(order=1, seed=3)
        model.fit(["नमस्ते विश्व नमस्ते ब्रह्म", "यह एक परीक्षण है"])
        return model

    def test_training_counts(self):
        model = self.make()
        assert model.is_trained()
        assert model.tokens == 8
        assert model.counts["नमस्ते"] == {"विश्व": 1, "ब्रह्म": 1}

    def test_generation_is_deterministic_with_seed(self):
        model = self.make()
        first = model.generate("नमस्ते", length=4)
        second = self.make().generate("नमस्ते", length=4)
        assert first == second
        assert first.startswith("नमस्ते")

    def test_generation_without_seed_starts_from_training_text(self):
        model = self.make()
        assert model.generate(length=2).split()[0] in {"नमस्ते", "यह"}

    def test_unseen_context_backs_off(self):
        model = self.make()
        text = model.generate("अज्ञात", length=3)
        assert text.startswith("अज्ञात")

    def test_perplexity_is_finite_and_positive(self):
        model = self.make()
        value = model.perplexity("नमस्ते विश्व")
        assert 0 < value < float("inf")

    def test_untrained_model_refuses(self):
        import brahma_ai

        with pytest.raises(ValueError):
            brahma_ai.MarkovModel().generate()
        with pytest.raises(ValueError):
            brahma_ai.MarkovModel(order=0)

    def test_save_and_load_roundtrip(self, tmp_path):
        import brahma_ai

        path = str(tmp_path / "model.json")
        model = self.make()
        model.save(path)
        loaded = brahma_ai.MarkovModel.load(path)
        assert loaded.counts == model.counts
        assert loaded.generate("नमस्ते", length=3) == model.generate("नमस्ते", length=3)

    @pytest.mark.parametrize(
        "prompt,template",
        [
            ("मुझे चैट ऐप चाहिए", "chat"),
            ("admin dashboard", "admin_chat"),
            ("health check", "status"),
        ],
    )
    def test_router(self, prompt, template):
        import brahma_ai

        assert brahma_ai.PromptRouter().route(prompt) == template

    def test_router_explains_itself(self):
        import brahma_ai

        template, matched = brahma_ai.PromptRouter().explain("मुझे चैट चाहिए")
        assert (template, matched) == ("chat", "चैट")
        assert brahma_ai.PromptRouter().explain("कुछ भी")[1] == "default"

    def test_generator_uses_the_router(self, tmp_path):
        path = brahma_auto.create_app("सिर्फ status चाहिए", base=str(tmp_path))
        assert os.path.isfile(os.path.join(path, "backend", "api.py"))
        assert not os.path.isfile(os.path.join(path, "backend", "server.py"))


# ---------------------------------------------------------------------------
# brahma_packaging: never claim a ZIP is an APK
# ---------------------------------------------------------------------------
class TestPackaging:
    def test_bundle_is_a_zip_and_says_so(self, tmp_path):
        import brahma_packaging

        source = tmp_path / "src"
        source.mkdir()
        (source / "index.html").write_text("<html></html>", encoding="utf-8")

        bundle = brahma_packaging.build_bundle("demo", [str(source)], str(tmp_path / "out"))
        assert os.path.isfile(bundle.path)
        assert bundle.path.endswith(".zip")
        assert bundle.is_apk is False
        assert not brahma_packaging.is_installable_apk(bundle.path)
        assert "ZIP" in bundle.summary()

    def test_text_file_named_apk_is_detected(self, tmp_path):
        import brahma_packaging

        fake = tmp_path / "fake.apk"
        fake.write_text("SANSKRIT APK\n", encoding="utf-8")
        assert brahma_packaging.describe(str(fake)) == "not a ZIP archive"
        assert not brahma_packaging.is_installable_apk(str(fake))

    def test_zip_with_placeholder_dex_is_not_installable(self, tmp_path):
        import brahma_packaging
        import zipfile

        fake = tmp_path / "fake.apk"
        with zipfile.ZipFile(fake, "w") as archive:
            archive.writestr("AndroidManifest.xml", "<manifest/>")
            archive.writestr("classes.dex", "sutra-dex")
            archive.writestr("META-INF/MANIFEST.MF", "")

        assert brahma_packaging.describe(str(fake)) == "ZIP archive (not an installable APK)"
        assert not brahma_packaging.is_installable_apk(str(fake))

    def test_builders_do_not_promise_apks(self):
        for path in ("engine/apk_builder.py", "engine/apk_builder_v2.py", "engine/apk_engine.py"):
            source = open(os.path.join(REPO_ROOT, path), encoding="utf-8").read()
            assert "os.system" not in source
            assert 'print("Installable APK' not in source
            assert 'print("APK सफलतया निर्मित' not in source
