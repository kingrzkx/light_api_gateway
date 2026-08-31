from fastapi import FastAPI

mock_app = FastAPI()

@mock_app.get("/api/demo")
def demo():
    return {"msg":"来自被代理后端的返回","code":200}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(mock_app, host="127.0.0.1", port=8080)
