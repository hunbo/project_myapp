import uvicorn

#terminal 실행: uvicorn app.main:app --reload

if __name__=="__main__":
    # uvicorn.run('main.app',host='localhost',port=9000, reload=True)
    # uvicorn.run('main.app',host='0.0.0.0',port=9000, reload=True)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)