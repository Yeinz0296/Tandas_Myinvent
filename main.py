import time, gsheet, tandas_perempuan, tandas_lelaki
from fastapi import Request, FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import FileResponse

# SETUP
app = FastAPI()
app.mount("/perempuan", WSGIMiddleware(tandas_perempuan.app.server))
#app.mount("/lelaki", WSGIMiddleware(tandas_lelaki.app.server))

# HTML PATH
html_index = 'index.html'

@app.get("/")
async def read_root():
    return FileResponse(html_index)

# @app.post("/tele")
# async def telebot():
#     return {"Telegram": "Bot"}

@app.post("/data_tandas/")
async def create_item(request: Request):
    jitem = await request.json()
    
    datetime = time.strftime('%m/%d/%Y %H:%M:%S')

    jitem_data = jitem['data']
    data=[datetime]

    for x in jitem_data.values():
        data.append(x)

    print(data)
    gsheet.wks.append_table([data])

    gsheet.save_to_csv()

    return jitem['data']
