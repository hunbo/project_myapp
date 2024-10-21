from fastapi import FastAPI, Request, Form, Depends, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import uvicorn
from database import engine,Sessionlocal
from sqlalchemy.orm import Session
import models
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse
import uvicorn
from starlette.status import HTTP_400_BAD_REQUEST
from face_recog import FaceRecog,video_process

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# 데이터베이스 세션을 생성하고 관리하는 역할.
def get_db():
    db = Sessionlocal()   # 데이터베이스와 연결하는 세션을 생성하는 함수.
    try:
        yield db   # fastapi에서 이 yield 문을 사용해서 데이터베이스 세션을 요청마다 생성하고, 요청이 끝나면 세션을 자동으로 닫도록 관리함.
    except:
        print("db연결 오류")
    finally:
        db.close()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory=f"static"), name="static")

@app.get("/")
async def home(request:Request): 
    
    return templates.TemplateResponse("index.html",
                                      {"request":request
                                       }
                                       )

# @app.post("/dashboard")
# async def add_sale(request:Request, month: int = Form(...), sales_amount: float = Form(...), db: Session = Depends(get_db)):
    
#     new_sale = models.Sales(month=month, sales_amount=sales_amount)
#     db.add(new_sale)
#     db.commit()
#     return RedirectResponse("/dashboard", status_code=303)

# @app.post("/dashboard")
# async def dup_sale(request:Request, db:Session=Depends(get_db),
#                    month:int = Form(...), sales_amount=Form(...)):
    
#     existing_month = db.query(models.Sales).filter(models.Sales.month == month).first()

#     if existing_month :
#         raise HTTPException(
#             status_code=HTTP_400_BAD_REQUEST,
#             detail=f"매출 데이터가 이미 존재합니다 : {month}"
#         )
    
#     new_sale = models.Sales(sales_amount=sales_amount, month=month)
#     db.add(new_sale)
#     db.commit()
#     return RedirectResponse("/dashboard", status_code=303)

@app.post("/dashboard", response_class=HTMLResponse)
async def dup_update_sales(request:Request, db:Session=Depends(get_db),
                           month:int = Form(...), sales_amount=Form(...)):
    existing_sale = db.query(models.Sales).filter(models.Sales.month == month).first()

    if existing_sale:
        existing_sale.sales_amount = sales_amount
        db.commit()
        db.refresh(existing_sale)
        message = f"{month}월의 매출 데이터가 업데이트되었습니다."
        print(message)

    else:
        new_sale = models.Sales(sales_amount=sales_amount,month=month)
        db.add(new_sale)
        db.commit()
        message=f"{month}월의 매출 데이터가 새로 추가되었습니다."
        print(message)

    return RedirectResponse("/dashboard", status_code=303)


@app.get("/dashboard")
async def get_dashboard(request:Request, db:Session = Depends(get_db)): 
    sales_datas = db.query(models.Sales).order_by(models.Sales.month.asc()).all()

    
    #message = "Hello, Welcome to my localhost dashboard."
    
    return templates.TemplateResponse("dashboard.html",
                                      {"request":request,
                                       "data":sales_datas
                                       }
                                       )

@app.get("/facerecog")
async def get_facerecog(request:Request, db:Session = Depends(get_db)): 
    # FaceRecog 인스턴스 생성
    face_recog_instance = FaceRecog()

    # 스트리밍 응답
    return StreamingResponse(video_process(face_recog_instance), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/facerecogview")
def get_video_page(request:Request):
    return templates.TemplateResponse("face_recog.html", {"request": request})







# ------------------ 밑에서부턴 todo -----------------------------


@app.get("/todo_list")
async def todo_home(request:Request, db_ss : Session = Depends(get_db)): #db:Session은 이 변수가 SQLAlchemy 세션 객체임을 명시.
    # Depends(get_db) : FastAPI는 Depends()를 통해 의존성 주입을 사용하여 get_db() 함수를 호출하고, 이 함수가 변환하는 값을 db_ss 변수에 할당.
    # db객체 생성, 세션 연갈하기 <- 의존성 주입으로 처리
    # 테이블 조회
    todos = db_ss.query(models.Todo) \
    .order_by(models.Todo.id.desc())
    # print(type(todos))

    #db 조회한 결과를 출력
    for todo in todos:
        print(todo.id, todo.task, todo.completed)
    return templates.TemplateResponse("todos/todo_list.html",
                                      {"request":request,
                                       "todos":todos
                                       })

@app.post("/add")
async def add(request:Request, task:str=Form(...), db_ss : Session = Depends(get_db) ):
    #여기의 task는 index.html에서 textarea name="task" 의 task임!

    # 클라이언트에서 textarea에서 입력 데이터 넘어오면
    # db 테이블에 저장하고 결과를 html에 랜더링에서 리턴
    print(task)
    # 클라이언트에게서 넘어온 task를 Todo 객체로 생성
    todo = models.Todo(task=task)
    # db 의존성 주입해서 처리함 Depends(get_db) : 엔진객체생성, 세션연결,
    db_ss.add(todo)
    # db에 실제로 저장, commit
    db_ss.commit()

    return RedirectResponse(url=app.url_path_for("todo_list"), status_code=status.HTTP_303_SEE_OTHER)

#todo 수정을 위한 데이터 조회
@app.get("/edit/{todo_id}")
async def edit(request:Request, todo_id:int, db:Session=Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id==todo_id).first() # query:데이터베이스에서 데이터를 조회
    return templates.TemplateResponse("todos/todo_edit.html", {"request": request, "todo": todo})

# todo 업데이트
@app.post("/edit/{todo_id}")
async def edit(request:Request, todo_id:int, task:str = Form(...), completed:bool = Form(False), db:Session=Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.task = task
    todo.completed = completed
    db.commit()
    return RedirectResponse(url=app.url_path_for("todo_home"), status_code=status.HTTP_303_SEE_OTHER)
    

@app.get("/delete/{todo_id}")  #라우팅, 주로 서버에서 데이터를 조회하거나, 특정 작업을 처리한 후에 리디렉션할 때 GET 요청을 함
async def delete(request:Request, todo_id:int, db:Session=Depends(get_db)):  #todo_id는 경로 매개변수
    todo = db.query(models.Todo).filter(models.Todo.id==todo_id).first() #.first(): 이 쿼리는 조건을 만족하는 항목 중 첫 번째 결과를 반환. 만약 조선을 만족하는 항목이 없으면 None을 반환
    db.delete(todo)
    db.commit()
    return RedirectResponse(url=app.url_path_for("todo_home"), status_code=status.HTTP_303_SEE_OTHER)

if __name__=="__main__":

    
    # uvicorn.run('main.app',host='localhost',port=9000, reload=True)
    # uvicorn.run('main.app',host='0.0.0.0',port=9000, reload=True)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)