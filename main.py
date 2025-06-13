import os
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
from dotenv import load_dotenv
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from schemas import ChatResponse
from callback import StreamingLLMCallbackHandler
from websockets.exceptions import ConnectionClosedOK
from query_data import get_chain

# Load the environment variables from the .env file
load_dotenv()

# Access the variables using os.environ
openai_api_key = os.environ.get("OPENAI_API_KEY")

templates = Jinja2Templates(directory="templates")

app = FastAPI()


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/test")
async def test_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    stream_handler = StreamingLLMCallbackHandler(websocket)
    qa_chain = get_chain(stream_handler)
    

    while True:
        try:
            # Receive and send back the client message
            user_msg = await websocket.receive_text()
            logging.info(f"User input: {user_msg}")
            resp = ChatResponse(sender="human", message=user_msg, type="stream")
            await websocket.send_json(resp.dict())

            # Construct a response
            start_resp = ChatResponse(sender="bot", message="", type="start")
            await websocket.send_json(start_resp.dict())

            # Send the message to the chain and feed the response back to the client
            output = await qa_chain.ainvoke(
                {
                    "input": user_msg,
                }
            )
            logging.info(f"Agent output: {output}")
            # Send the agent's message to the client
            if hasattr(output, 'content'):
                agent_message = output.content
            elif isinstance(output, dict) and 'content' in output:
                agent_message = output['content']
            else:
                agent_message = output
            # Ensure agent_message is a string
            if not isinstance(agent_message, str):
                agent_message = str(agent_message)
            resp = ChatResponse(sender="bot", message=agent_message, type="stream")
            await websocket.send_json(resp.dict())
            # Send the end-response back to the client
            end_resp = ChatResponse(sender="bot", message="", type="end")
            await websocket.send_json(end_resp.dict())
        except WebSocketDisconnect:
            logging.info("WebSocketDisconnect")
            # TODO try to reconnect with back-off
            break
        except ConnectionClosedOK:
            logging.info("ConnectionClosedOK")
            # TODO handle this?
            break
        except Exception as e:
            logging.error(e)
            resp = ChatResponse(
                sender="bot",
                message="Sorry, something went wrong. Try again.",
                type="error",
            )
            await websocket.send_json(resp.dict())
