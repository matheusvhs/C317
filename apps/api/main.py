from fastapi import FastAPI

app = FastAPI(title="Observatório do Turismo de SRS")


@app.get("/api/v1/meta/atualizacao")
def atualizacao():
    return {"versao": "0.0.1", "gerado_em": "2026-09-04"}
