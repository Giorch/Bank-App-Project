from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.customerController import router as customerRouter
from controllers.accountController import router as accountRouter


app = FastAPI(
    title="Bank App REST API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
     allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customerRouter)
app.include_router(accountRouter)